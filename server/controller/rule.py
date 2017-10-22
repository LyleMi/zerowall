#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web

from server.controller.base import BaseHandler
from schema.tables.http import HTTP


class RuleHandler(BaseHandler):

    def get(self):
        return self.ok(HTTP.getAll(self.db, toStr=True))
    
    def delete(self):
        uid = self.get_argument('uid', '')
        HTTP.delete(self.db, uid)
        return self.ok("delete suc")