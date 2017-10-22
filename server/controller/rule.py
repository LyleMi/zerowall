#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web

from server.controller.base import BaseHandler
from schema.tables.http import HTTP


class RuleHandler(BaseHandler):

    def get(self):
        return self.ok(HTTP.getAll(self.db, toStr=True))
