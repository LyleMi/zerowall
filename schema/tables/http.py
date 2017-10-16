#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sqlalchemy import and_

from sqlalchemy import Column, BOOLEAN, VARCHAR

from orm.tables.base import BaseTable


class HTTP(BaseTable):

    __tablename__ = 'http'

    uid = Column(VARCHAR(32))
    key = Column(VARCHAR(200))
    value = Column(VARCHAR(200))
    rtype = Column(VARCHAR(10))
    allow = Column(BOOLEAN)

    @classmethod
    def addHTTP(cls, db, key, value, rtype, allow):
        http = HTTP()
        http.key = key
        http.value = value
        http.rtype = rtype
        http.allow = allow
        db.add(http)
        return True

    @classmethod
    def deleteHTTP(cls, db, uid):
        http = db.query(cls).filter(cls.uid == uid)
        if http.count() < 1:
            return None
        else:
            db.delete(http)
            return True

    @classmethod
    def changeHTTP(cls, db, uid, key, value, rtype, allow):
        http = db.query(cls).filter(cls.uid == uid)
        if http.count() < 1:
            return None
        else:
            http.key = key
            http.value = value
            http.rtype = rtype
            http.allow = allow
            db.update(http)
            return True

    @classmethod
    def getHTTP(cls, db, uid):
        http = db.query(cls).filter(cls.uid == uid)
        if http.count() < 1:
            return None
        else:
            return http.one()
