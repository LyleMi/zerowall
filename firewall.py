#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

from common.logger import logfmt
from firewall.handler import HTTP


def main():
    parser = argparse.ArgumentParser(
        description='Simple Python Application Firewall',
        epilog='Simple Python Application Firewall'
    )

    parser.add_argument('--webhost', default='127.0.0.1',
                        help='Default: 127.0.0.1')
    parser.add_argument('--webport', default='80', help='Default: 80')
    parser.add_argument('--srvhost', default='127.0.0.1',
                        help='Default: 127.0.0.1')
    parser.add_argument('--srvport', default='8083', help='Default: 8083')
    parser.add_argument('--log-level', default='INFO',
                        help='DEBUG, INFO, WARNING, ERROR, CRITICAL')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level),
                        format=logfmt)

    webhost = args.webhost
    webport = int(args.webport)
    srvhost = args.srvhost
    srvport = int(args.srvport)

    proxy = HTTP(srvhost, srvport, webhost, webport)
    proxy.run()

if __name__ == '__main__':
    main()
