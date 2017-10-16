#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sqlalchemy import and_

from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy import TIMESTAMP, TEXT, Enum

from orm.tables.base import BaseTable


class Log(BaseTable):

    __tablename__ = 'log'

    uid = Column(VARCHAR(32), primary_key=True)
    srcip = Column(VARCHAR(200))
    url = Column(VARCHAR(500))
    full = Column(TEXT)
    resp = Column(TEXT)
    time = Column(TIMESTAMP)

    @classmethod
    def addLog(cls, db, uid, content):
        log = Log()
        return True
