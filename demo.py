#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
from utils.logger import logger

# from ping import Ping
# from tcping import TCPing
# from tlsping import TLSPing
from mtr import MTR

stdHandler = logger.handlers[0]
stdHandler.setLevel(logging.DEBUG)

# p = Ping('ip.343.re')
# p = Ping('255.255.255.255')
# p.count = 4
# p.run()

# p = TCPing('8.210.148.24', 443)
# p.run()

# p = TLSPing('8.210.148.24', 443)
# p.run()

p = MTR('8.210.148.24')
p.run()
