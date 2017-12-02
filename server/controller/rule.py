#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web

from server.controller.base import BaseHandler
from schema.tables.http import HTTP


class RuleHandler(BaseHandler):

    def get(self):
        return self.ok(HTTP.getAll(self.db, toStr=True))

    def post(self):
        key = self.get_argument('key')
        value = self.get_argument('value')
        rtype = self.get_argument('rtype')
        seq = self.get_argument('seq')
        allow = self.get_argument('allow') == '1'
        HTTP.add(self.db, key, value, rtype, allow)
        return self.ok(HTTP.getAll(self.db, toStr=True))

    def put(self):
        uid = self.get_argument('uid')
        key = self.get_argument('key')
        value = self.get_argument('value')
        rtype = self.get_argument('rtype')
        seq = self.get_argument('seq')
        allow = self.get_argument('allow') == '1'
        HTTP.change(self.db, uid, key, value, rtype, allow)
        return self.ok("suc")

    def delete(self):
        uid = self.get_argument('uid', '')
        HTTP.delete(self.db, uid)
        return self.ok("delete suc")
