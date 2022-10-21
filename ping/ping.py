#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils import logger
from utils import checker

from utils import isHost
from utils import runProcess

class Ping:
    """Netools ping module

    Attributes:
        server: Ping package target. (ipv4 / ipv6 / domain)
        v6First: IPv6 is preferred. (server -> domain name)
        count: The number of ping requests sent. (1 ~ 64)
        fast: Ping as soon as reply is received.
        size: Data bytes in packets. (4 ~ 1016)
        timeout: Time limit for all requests. (1 ~ 60)
    """
    rules = [
        ('server', str, isHost),
        ('v6First', bool, None),
        ('count', int, lambda x: 1 <= x <= 64),
        ('fast', bool, None),
        ('size', int, lambda x: 4 <= x <= 1016),
        ('timeout', int, lambda x: 1 <= x <= 60),
    ]

    def __valueInit(self) -> None:  # load default value
        self.v6First = False
        self.count = 16
        self.fast = True
        self.size = 56
        self.timeout = 20

    def __valueCheck(self) -> None:
        checker('Ping', self.rules,
            self.server, self.v6First, self.count, self.fast, self.size, self.timeout
        )

    def __valueDump(self) -> None:
        logger.debug('[%s] Ping server -> %s' % (self.id, self.server))
        logger.debug('[%s] Ping v6First -> %s' % (self.id, self.v6First))
        logger.debug('[%s] Ping count -> %d' % (self.id, self.count))
        logger.debug('[%s] Ping fast -> %s' % (self.id, self.fast))
        logger.debug('[%s] Ping size -> %d' % (self.id, self.size))
        logger.debug('[%s] Ping timeout -> %d' % (self.id, self.timeout))

    def __runPing(self) -> str:  # ping command raw output
        pingCmd = [
            'ping', self.server,
            '-c', str(self.count),
            '-s', str(self.size),
            '-w', str(self.timeout),
        ]
        if self.fast:  # enabled fast mode
            pingCmd.append('-A')
        process = runProcess(pingCmd)
        process.wait()  # wait ping process exit
        return process.stdout.read().decode()

    def __init__(self, server: str) -> None:
        # TODO: generate task ID
        self.id = '233333'
        self.__valueInit()
        self.server = server

    def run(self):
        self.__valueCheck()
        self.__valueDump()

        raw = self.__runPing()

        print(raw)
        # TODO: server -> ip address
        # TODO: ping process
