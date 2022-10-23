#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ping import Ping
from tcping import TCPing
from tlsping import TLSPing

# p = Ping('ip.343.re')
# p.run()

# p = TCPing('8.210.148.24', 443)
# p.run()

p = TLSPing('8.210.148.24', 443)
p.run()
