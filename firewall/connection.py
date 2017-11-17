#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

from common.logger import logger


class Connection(object):

    """
    TCP server/client connection abstraction.
    """

    def __init__(self, what):
        self.buffer = b''
        self.closed = False
        self.what = what  # server or client

    def send(self, data):
        return self.conn.send(data)

    def recv(self, bytes=8192):
        try:
            data = self.conn.recv(bytes)
            if len(data) == 0:
                logger.debug('recvd 0 bytes from %s' % self.what)
                return None
            logger.debug('rcvd %d bytes from %s' % (len(data), self.what))
            return data
        except Exception as e:
            logger.exception(
                'Exception while receiving from connection %s %r with reason %r' %
                (self.what, self.conn, e)
            )
            return None

    def close(self):
        self.conn.close()
        self.closed = True

    def buffer_size(self):
        return len(self.buffer)

    def has_buffer(self):
        return self.buffer_size() > 0

    def queue(self, data):
        self.buffer += data

    def flush(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
        logger.debug('flushed %d bytes to %s' % (sent, self.what))


class Server(Connection):

    """
    Establish connection to destination server.
    """

    def __init__(self, host, port):
        super(Server, self).__init__(b'server')
        self.addr = (host, int(port))
        # self.addr = ("127.0.0.1", 80)

    def connect(self):
        # print(self.addr)
        # self.addr[0] = "127.0.0.1"
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.addr[0], self.addr[1]))


class Client(Connection):

    """
    Accepted client connection.
    """

    def __init__(self, conn, addr):
        super(Client, self).__init__(b'client')
        self.conn = conn
        self.addr = addr
