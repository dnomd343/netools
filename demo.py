#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ping import Ping
from tcping import Tcping

# p = Ping('ip.343.re')
# p.run()

p = Tcping('8.210.148.24', 443)
p.run()
