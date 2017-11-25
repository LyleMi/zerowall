#!/usr/bin/env python
# -*- coding: utf-8 -*-

import select
import datetime
import multiprocessing

from common.core import initDB
from common.logger import logger
from firewall.const import *
from firewall.parser import HttpParser
from firewall.connection import Server
from firewall.error import ProxyConnectionFailed
from schema.tables.log import Log


class Proxy(multiprocessing.Process):

    """
    HTTP proxy implementation.
    Accepts connection object and act as a proxy
    between client and server.
    """

    def __init__(self, client, server):
        super(Proxy, self).__init__()
        self.start_time = self._now()
        self.last_activity = self.start_time

        self.client = client
        self.server = server
        self.server.closed = True

        self.request = HttpParser()
        self.response = HttpParser(HTTP_RESPONSE_PARSER)

        self.connection_established_pkt = CRLF.join([
            b'HTTP/1.1 200 Connection established',
            b'Proxy-agent: proxy.py',
            CRLF
        ])

    def _now(self):
        return datetime.datetime.utcnow()

    def _inactive_for(self):
        return (self._now() - self.last_activity).seconds

    def _is_inactive(self):
        return self._inactive_for() > 30

    def _client_reject(self):
        self.client.queue(CRLF.join([
            b'HTTP/1.1 502 Bad Gateway',
            b'Proxy-agent: proxy.py',
            b'Content-Length: 11',
            b'Connection: close',
            CRLF
        ]) + b'Bad Gateway')
        self.client.flush()

    def _process_request(self, data):
        # once we have connection to the server
        # we don't parse the http request packets
        # any further, instead just pipe incoming
        # data from client to server
        if self.server and not self.server.closed:
            self.server.queue(data)
            return

        # parse http request
        self.request.parse(data)

        # once http request parser has reached the state complete
        # we attempt to establish connection to destination server
        if self.request.state == HTTP_PARSER_STATE_COMPLETE:
            logger.debug('request parser is in state complete')

            try:
                host = self.server.addr[0]
                port = self.server.addr[1]
                logger.debug('connecting to server %s:%s' % (host, port))
                self.server.closed = False
                self.server.connect()
                logger.debug('connected to server %s:%s' % (host, port))
            except Exception as e:
                self.server.closed = True
                raise ProxyConnectionFailed(host, port, repr(e))

            # for http connect methods (https requests)
            # queue appropriate response for client
            # notifying about established connection
            if self.request.method == b"CONNECT":
                self.client.queue(self.connection_established_pkt)
            # for usual http requests, re-build request packet
            # and queue for the server with appropriate headers
            else:
                self.server.queue(self.request.build(
                    del_headers=[b'proxy-connection',
                                 b'connection', b'keep-alive'],
                    add_headers=[(b'Connection', b'Close')]
                ))

    def _process_response(self, data):
        # parse incoming response packet
        # only for non-https requests
        if not self.request.method == b"CONNECT":
            self.response.parse(data)

        # queue data for client
        self.client.queue(data)

    def _access_log(self):
        host, port = self.server.addr if self.server else (None, None)
        if self.request.method == b"CONNECT":
            logger.info(
                "%s:%s - %s %s:%s" %
                (
                    self.client.addr[0],
                    self.client.addr[1],
                    self.request.method,
                    host, port
                )
            )
        elif self.request.method:
            logger.info(
                "%s:%s - %s %s:%s%s - %s %s - %s bytes" % (
                    self.client.addr[0],
                    self.client.addr[1],
                    self.request.method.decode("utf8"),
                    host, port,
                    self.request.build_url().decode("utf8"),
                    self.response.code.decode("utf8"),
                    self.response.reason.decode("utf8"),
                    len(self.response.raw)
                )
            )
            Log.add(
                self.db,
                ":".join(map(str, self.client.addr)),
                self.request.build_url().decode("utf8"),
                self.request.method.decode("utf8"),
                self.response.code.decode("utf8") +
                " " + self.response.reason.decode("utf8")
            )

    def _get_waitable_lists(self):
        rlist, wlist, xlist = [self.client.conn], [], []
        logger.debug('*** watching client for read ready')

        if self.client.has_buffer():
            logger.debug('pending client buffer found,' +
                         ' watching client for write ready')
            wlist.append(self.client.conn)

        if self.server and not self.server.closed:
            logger.debug(
                'connection to server exists,' +
                ' watching server for read ready'
            )
            rlist.append(self.server.conn)

        if self.server and not self.server.closed and self.server.has_buffer():
            logger.debug(
                'connection to server exists and ' +
                'pending server buffer found, ' +
                'watching server for write ready'
            )
            wlist.append(self.server.conn)

        return rlist, wlist, xlist

    def _process_wlist(self, w):
        if self.client.conn in w:
            logger.debug('client is ready for writes, flushing client buffer')
            self.client.flush()

        if self.server and not self.server.closed and self.server.conn in w:
            logger.debug('server is ready for writes, flushing server buffer')
            self.server.flush()

    def _process_rlist(self, r):
        if self.client.conn in r:
            logger.debug('client is ready for reads, reading')
            data = self.client.recv()
            self.last_activity = self._now()

            if not data:
                logger.debug('client closed connection, breaking')
                return True

            try:
                self._process_request(data)
            except ProxyConnectionFailed as e:
                logger.exception(e)
                self._client_reject()
                return True

        if self.server and not self.server.closed and self.server.conn in r:
            logger.debug('server is ready for reads, reading')
            data = self.server.recv()
            self.last_activity = self._now()

            if not data:
                logger.debug('server closed connection')
                self.server.close()
            else:
                self._process_response(data)

        return False

    def _process(self):
        while True:
            rlist, wlist, xlist = self._get_waitable_lists()
            r, w, x = select.select(rlist, wlist, xlist, 1)
            self._process_wlist(w)
            '''
            self._reject_client() if needed
            '''
            if self._process_rlist(r):
                break

            if self.client.buffer_size() == 0:
                if self.response.state == HTTP_PARSER_STATE_COMPLETE:
                    logger.debug(
                        'client buffer is empty and ' +
                        'response state is complete, breaking'
                    )
                    break

                if self._is_inactive():
                    logger.debug(
                        'client buffer is empty and ' +
                        'maximum inactivity has reached, breaking'
                    )
                    break

    def run(self):
        self.db = initDB()
        logger.debug(
            'Proxying connection %r at address %r' %
            (self.client.conn, self.client.addr)
        )
        try:
            self._process()
        except Exception as e:
            logger.exception(
                'Exception while handling connection %r with reason %r' %
                (self.client.conn, e)
            )
        finally:
            logger.debug(
                "closing connection with pending client %d bytes buffer" %
                self.client.buffer_size()
            )
            self.client.close()
            if self.server:
                logger.debug(
                    "closed connection with pending server %d bytes buffer" %
                    self.server.buffer_size()
                )
            self._access_log()
            logger.debug('Closing proxy for connection %r at address %r' %
                         (self.client.conn, self.client.addr))
