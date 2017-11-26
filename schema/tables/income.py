#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import Column, BOOLEAN, VARCHAR, INT
from sqlalchemy.sql import func

from schema.tables.base import BaseTable
from common.utils import guid
from common.utils import isSubnet


class Income(BaseTable):

    __tablename__ = 'income'

    uid = Column(VARCHAR(32), primary_key=True, default=guid)
    seq = Column(INT)
    ip = Column(VARCHAR(64))
    allow = Column(BOOLEAN)
    comment = Column(VARCHAR(200))

    @classmethod
    def add(cls, db, ip, allow, comment="", seq=0):
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
        income = Income(
            ip=ip, allow=allow,
            comment=comment, seq=seq
        )
        db.add(income)
        db.commit()
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
        db.commit()
        return True

    @classmethod
    def getNewSeq(cls, db):
        ret = db.query(func.max(cls.seq)).one()[0]
        return 0 if ret is None else ret + 1

    @classmethod
    def isAllowed(cls, db, ip):
        for rule in db.query(cls).order_by(cls.seq.asc()).all():
            if isSubnet(ip, rule.ip):
                return rule.allow
        return True
