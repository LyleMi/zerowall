#!/usr/bin/env python
# -*- coding:utf-8 -*-

from copy import deepcopy

from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class BaseTable(object):

    def toStr(self):
        s = deepcopy(self.__dict__)
        del(s['_sa_instance_state'])
        return s

    @classmethod
    def getAll(cls, db):
        return db.query(cls).all()

    @classmethod
    def get(cls, db, uid):
        obj = db.query(cls).filter(cls.uid == uid)
        if obj.count() < 1:
            return None
        else:
            return obj.one()

    @classmethod
    def delete(cls, db, uid):
        obj = db.query(cls).filter(cls.uid == uid).delete()
        return True
