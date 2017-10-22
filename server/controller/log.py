#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web

from server.controller.base import BaseHandler
from schema.tables.log import Log


class LogHandler(BaseHandler):

    def get(self):
        return self.ok(Log.getAll(self.db, toStr=True))
    
    def delete(self):
        uid = self.get_argument('uid', '')
        Log.delete(self.db, uid)
        return self.ok("delete suc")
