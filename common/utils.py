#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import random
import re
import uuid
from functools import reduce


def guid():
    return uuid.uuid4().hex


def ip2num(ip):
    return reduce(lambda x, y: x*256+y, map(int, ip.split(".")))


def isSubnet(ip, subnet):
    subnet = subnet.split("/")
    if len(subnet) != 2:
        return ip == subnet[0]
    ip = ip2num(ip)
    subnetip = subnet[0]
    mask = int(("1" * int(subnet[1])).ljust(32, "0"), 2)
    return (ip & mask) == (ip2num(subnetip) & mask)

if __name__ == '__main__':
    print(isSubnet("127.0.0.1", "127.0.0.0/24"))
    print(isSubnet("127.0.0.1", "127.0.0.5/24"))
    print(isSubnet("127.0.0.1", "127.0.1.5/24"))
    print(isSubnet("192.167.1.1", "127.0.1.5/24"))
    print(isSubnet("192.167.1.1", "127.0.1.5/0"))
    print(isSubnet("192.167.1.1", "192.167.1.0/31"))
    print(isSubnet("192.167.1.1", "192.167.1.0/31"))
    print(isSubnet("192.167.1.1", "192.167.1.0/32"))
    print(isSubnet("192.167.1.1", "192.167.1.0"))
    print(isSubnet("192.167.1.1", "192.167.1.1"))
