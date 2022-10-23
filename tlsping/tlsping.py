#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils import logger
from utils import checker
from utils import genFlag
from utils import isPort, isHost

class TlsPing:
    """Netools tlsping module

    Attributes:
        server: TlsPing package target. (ipv4 / ipv6 / domain)
        port: TCP port for connection. (1 ~ 65535)
        host: SNI parameter in TLS connection. (using server in default)
        v6First: IPv6 is preferred. (server -> domain name)
        verify: Make sure tls is not subject to MITM attacks.
        count: The number of tls connection tried. (1 ~ 16)
    """
    rules = [  # parameter rules
        ('server', str, isHost),
        ('port', int, isPort),
        ('host', str, None),
        ('v6First', bool, None),
        ('verify', bool, None),
        ('count', int, lambda x: 1 <= x <= 16),
    ]

    def __valueInit(self) -> None:  # load default values
        self.host = ''
        self.v6First = False
        self.verify = True
        self.count = 4

    def __valueCheck(self) -> None:  # check parameter values
        checker('TlsPing', self.rules,
            self.server, self.port, self.host, self.v6First, self.verify, self.count
        )

    def __valueDump(self) -> None:  # output parameter values
        logger.debug('[%s] TlsPing server -> %s' % (self.id, self.server))
        logger.debug('[%s] TlsPing port -> %d' % (self.id, self.port))
        logger.debug('[%s] TlsPing host -> %s' % (self.id, self.host))
        logger.debug('[%s] TlsPing v6First -> %s' % (self.id, self.v6First))
        logger.debug('[%s] TlsPing verify -> %s' % (self.id, self.verify))
        logger.debug('[%s] TlsPing count -> %d' % (self.id, self.count))

    def __init__(self, server: str, port: int) -> None:
        self.id = genFlag()
        self.__valueInit()
        self.server = server  # load ping server
        self.port = port # load tcping port
        logger.debug('[%s] TlsPing task init -> %s(:%d)' % (self.id, self.server, self.port))

