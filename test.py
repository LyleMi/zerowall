#!/usr/bin/env python
# -*- coding:utf-8 -*-

from common.core import initDB
from schema.tables.http import HTTP
from schema.tables.income import Income
from schema.tables.log import Log


def testHTTP(db):
    uid = ""
    print HTTP.add(db, "header", "sqlmap", "contain", 0)

    for h in HTTP.getAll(db):
        uid = h.uid
        print h.toStr()

    print HTTP.get(db, uid).toStr()

    print HTTP.change(db, uid, value='wvs')

    print HTTP.get(db, uid).toStr()

    print HTTP.delete(db, uid)

    db.commit()


def testIncome(db):
    uid = ""
    print Income.add(db, "192.168.1.0/24", 0, "internat")

    for i in Income.getAll(db):
        uid = i.uid
        print i.toStr()

    print Income.get(db, uid).toStr()

    print Income.change(db, uid, comment='new comment')

    print Income.get(db, uid).toStr()

    print Income.delete(db, uid)

    db.commit()


def testLog(db):
    uid = ""
    print Log.add(db, "192.168.1.124", "http://t.cn",
                  "request", "response")

    for l in Log.getAll(db):
        uid = l.uid
        print l.toStr()

    print Log.get(db, uid).toStr()

    print Log.delete(db, uid)

    db.commit()

if __name__ == '__main__':
    db = initDB()
    testHTTP(db)
    testIncome(db)
    testLog(db)
