#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from common.core import initDB
from common.logger import logger
from firewall.connection import Client, Server
from firewall.proxy import Proxy
from schema.tables.income import Income


class TCP(object):

    """
    TCP server implementation.
    """

    def __init__(self, host='127.0.0.1', port=8083,
                 webhost='127.0.0.1', webport=80, backlog=100):
        self.host = host
        self.port = port
        self.webhost = webhost
        self.webport = webport
        self.backlog = backlog
        self.db = initDB()

    def handle(self, client, server):
        raise NotImplementedError()

    def run(self):
        try:
            logger.info('Starting server on port %d' % self.port)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.backlog)
            while True:
                conn, addr = self.socket.accept()
                logger.debug('Accepted connection %r at address %r' %
                             (conn, addr))
                if not Income.isAllowed(self.db, addr[0]):
                    conn.close()
                else:
                    client = Client(conn, addr)
                    server = Server(self.webhost, self.webport)
                    self.handle(client, server)
                # flush
                self.db.close()
                self.db = initDB()
        except Exception as e:
            logger.exception('Exception while running the server %r' % e)
        finally:
            logger.info('Closing server socket')
            self.socket.close()


class HTTP(TCP):

    """
    HTTP firewall implementation.
    Spawns new process to proxy accepted client connection.
    """

    def handle(self, client, server):
        proc = Proxy(client, server)
        proc.daemon = True
        proc.start()
        logger.debug(
            'Started process %r to handle connection %r' %
            (proc, client.conn)
        )
