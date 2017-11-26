#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web

from server.controller.base import BaseHandler
from schema.tables.income import Income


class BlistHandler(BaseHandler):

    def get(self):
        return self.ok(Income.getAll(self.db, toStr=True))

    def post(self):
        ip = self.get_argument('ip')
        allow = self.get_argument('allow') == '1'
        comment = self.get_argument('comment')
        seq = self.get_argument('seq')
        Income.add(self.db, ip, allow, comment, seq)
        # self.db.commit()
        return self.ok(Income.getAll(self.db, toStr=True))

    def delete(self):
        uid = self.get_argument('uid', '')
        Income.delete(self.db, uid)
        return self.ok("delete suc")
