#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy import TIMESTAMP, TEXT, Enum

from schema.tables.base import BaseTable
from common.utils import guid


class Log(BaseTable):

    __tablename__ = 'log'

    uid = Column(VARCHAR(32), primary_key=True, default=guid)
    client = Column(VARCHAR(200))
    url = Column(VARCHAR(500))
    method = Column(VARCHAR(10))
    time = Column(TIMESTAMP)
    ret = Column(VARCHAR(20))
    full = Column(TEXT)
    resp = Column(TEXT)

    @classmethod
    def add(cls, db, client, url, method, ret):
        db.add(Log(
            client=client, url=url,
            method=method, ret=ret
        ))
        db.commit()
        return True
