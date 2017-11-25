#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import and_
from sqlalchemy import Column, BOOLEAN, VARCHAR, INT

from schema.tables.base import BaseTable
from common.utils import guid


class HTTP(BaseTable):

    __tablename__ = 'http'

    uid = Column(VARCHAR(32), primary_key=True, default=guid)
    seq = Column(INT)
    key = Column(VARCHAR(200))
    value = Column(VARCHAR(200))
    rtype = Column(VARCHAR(10))
    allow = Column(BOOLEAN)

    @classmethod
    def add(cls, db, key, value, rtype, allow):
        http = HTTP()
        http.key = key
        http.value = value
        http.rtype = rtype
        http.allow = allow
        db.add(http)
        db.commit()
        return True

    @classmethod
    def change(cls, db, uid, key=None,
                   value=None, rtype=None, allow=None):
        updateobj = {}
        if key is not None:
            updateobj[cls.key] = key
        if value is not None:
            updateobj[cls.value] = value
        if rtype is not None:
            updateobj[cls.rtype] = rtype
        if allow is not None:
            updateobj[cls.allow] = allow
        http = db.query(cls).filter(cls.uid == uid).update(updateobj)
        db.commit()
        return True