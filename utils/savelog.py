#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

sys.path.append(os.path.join(".."))

from common.core import initDB
from schema.tables.log import Log

db = initDB()

logdir = os.path.join("..", "logs")
logpath = os.path.join(logdir, "firewall.log")
logfile = open(logpath)

for l in logfile:
    time = l[1:20]
    tmp = l[33:].split(" - ")
    client = tmp[0]
    method = tmp[1].split(" ")[0]
    url = tmp[1].split(" ")[1]
    ret = tmp[2]
    print time, client, method, url, ret
    Log.add(db, client, url, method, ret, time)

db.commit()
