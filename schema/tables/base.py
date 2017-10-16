#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import and_

from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy import TIMESTAMP, TEXT, Enum

from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class BaseTable(object):

    def toStr(self):
        s = self.__dict__
        del(s['_sa_instance_state'])
        return s
