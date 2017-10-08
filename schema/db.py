#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
from common.sqlconfig import mysql


class DB(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host=mysql['host'],
                                    user=mysql['user'],
                                    passwd=mysql['pass'],
                                    db=mysql['db'],
                                    charset='utf8')
        self.cur = self.conn.cursor()
