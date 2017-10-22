#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web

from server.controller.base import BaseHandler
from schema.tables.log import Log


class LogHandler(BaseHandler):

    def get(self):
        return self.ok(Log.getAll(self.db, toStr=True))
