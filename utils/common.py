#!/usr/bin/env python
# -*- coding:utf-8 -*-


def ip2num(ip):
    return reduce(lambda x, y: x*256+y, map(int, ip.split(".")))


def isSubnet(ip, subnet):
    ip = ip2num(ip)
    subnet = subnet.split("/")
    subnetip = subnet[0]
    mask = int(("1" * int(subnet[1])).ljust(32, "0"), 2)
    return (ip & mask) == (ip2num(subnetip) & mask)

if __name__ == '__main__':
    print isSubnet("127.0.0.1", "127.0.0.0/24")
    print isSubnet("127.0.0.1", "127.0.0.5/24")
    print isSubnet("127.0.0.1", "127.0.1.5/24")
    print isSubnet("192.167.1.1", "127.0.1.5/24")
    print isSubnet("192.167.1.1", "127.0.1.5/0")
    print isSubnet("192.167.1.1", "192.167.1.0/31")
    print isSubnet("192.167.1.1", "192.167.1.0/31")
    print isSubnet("192.167.1.1", "192.167.1.0/32")