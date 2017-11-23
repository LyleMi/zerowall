#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy import TIMESTAMP, TEXT, Enum

from schema.tables.base import BaseTable
from common.utils import guid


class Log(BaseTable):

    __tablename__ = 'log'

    uid = Column(VARCHAR(32), primary_key=True, default=guid)
    srcip = Column(VARCHAR(200))
    url = Column(VARCHAR(500))
    method = Column(VARCHAR(10))
    full = Column(TEXT)
    resp = Column(TEXT)
    time = Column(TIMESTAMP)

    @classmethod
    def add(cls, db, srcip, url, method, full, resp):
        log = Log(
            srcip=srcip, url=url, method=method,
            full=full, resp=resp
        )
        db.add(log)
        return True
