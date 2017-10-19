#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import Column, BOOLEAN, VARCHAR

from schema.tables.base import BaseTable
from common.utils import guid


class Income(BaseTable):

    __tablename__ = 'income'

    uid = Column(VARCHAR(32), primary_key=True, default=guid)
    ip = Column(VARCHAR(64))
    allow = Column(BOOLEAN)
    comment = Column(VARCHAR(200))

    @classmethod
    def add(cls, db, ip, allow, comment=""):
        income = Income(ip=ip, allow=allow, comment=comment)
        db.add(income)
        return True

    @classmethod
    def change(cls, db, uid, ip=None,
               allow=None, comment=None):
        updateobj = {}
        if ip is not None:
            updateobj[cls.ip] = ip
        if allow is not None:
            updateobj[cls.allow] = allow
        if comment is not None:
            updateobj[cls.comment] = comment
        income = db.query(cls).filter(cls.uid == uid).update(updateobj)
        return True
