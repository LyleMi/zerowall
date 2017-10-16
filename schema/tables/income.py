#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sqlalchemy import and_

from sqlalchemy import Column, BOOLEAN, VARCHAR

from orm.tables.base import BaseTable


class Income(BaseTable):

    __tablename__ = 'income'

    uid = Column(VARCHAR(32), primary_key=True)
    ip = Column(VARCHAR(64))
    allow = Column(BOOLEAN)
    comment = Column(VARCHAR(200))

    @classmethod
    def addIncome(cls, ip, allow, comment=""):
        income = Income(ip, allow, comment)
        db.add(income)
        return True

    @classmethod
    def getIncomes(cls):
        incomes = db.query(cls)
        if incomes.count() < 1:
            return None
        else:
            return incomes
