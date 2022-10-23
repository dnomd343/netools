#!/usr/bin/env python3
# -*- coding:utf-8 -*-

class Tcping:
    """Netools tcping module

    Attributes:
        server: Ping package target. (ipv4 / ipv6 / domain)
        port: TCP port for connection. (1 ~ 65535)
        v6First: IPv6 is preferred. (server -> domain name)
        count: The number of tcp connection tried. (1 ~ 16)
        timeout: Time limit for each connection. (1 ~ 10)
    """
