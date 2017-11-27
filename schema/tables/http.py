#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import and_
from sqlalchemy import Column, BOOLEAN, VARCHAR, INT
from sqlalchemy.sql import func

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
    def add(cls, db, key, value, rtype, allow, seq=0):
        if not seq:
            seq = cls.getNewSeq(db)
        else:
            others = db.query(cls).filter(
                cls.seq >= seq
            ).order_by(
                cls.seq.desc()
            ).all()
            for o in others:
                db.query(cls).filter(
                    cls.uid == o.uid
                ).update({
                    cls.seq: cls.seq+1
                })
        http = HTTP()
        http.key = key
        http.value = value
        http.rtype = rtype
        http.allow = allow
        http.seq = seq
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

    @classmethod
    def getNewSeq(cls, db):
        ret = db.query(func.max(cls.seq)).one()[0]
        return 0 if ret is None else ret + 1

    @classmethod
    def isAllowed(cls, db, method, url, headers):
        method = method.decode("utf8")
        url = url.decode("utf8")
        for rule in db.query(cls).order_by(cls.seq.asc()).all():
            if rule.key == "header":
                k, v = rule.value.split("|")
                k = k.lower().encode("utf8")
                if k in headers.keys():
                    if rule.rtype == "contain" and v in headers[k][1].decode("utf8"):
                        return rule.allow
                    elif rule.rtype == "equal" and v == headers[k][1].decode("utf8"):
                        return rule.allow
            elif rule.key == "method":
                if rule.value == method:
                    return rule.allow
            elif rule.key == "url":
                if rule.rtype == "contain" and rule.value in url:
                    return rule.allow
                if rule.rtype == "equal" and rule.value == url:
                    return rule.allow
        return True
