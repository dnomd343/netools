#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils import logger
from utils import checker
from utils import genFlag
from utils import host2IP
from utils import runProcess
from utils import isHost, isPort


class Tcping:
    """Netools tcping module

    Attributes:
        server: Ping package target. (ipv4 / ipv6 / domain)
        port: TCP port for connection. (1 ~ 65535)
        v6First: IPv6 is preferred. (server -> domain name)
        count: The number of tcp connection tried. (1 ~ 16)
        timeout: Time limit for each connection. (1 ~ 10)
    """
    rules = [  # parameter rules
        ('server', str, isHost),
        ('port', int, isPort),
        ('v6First', bool, None),
        ('count', int, lambda x: 1 <= x <= 16),
        ('timeout', int, lambda x: 1 <= x <= 10),
    ]

    def __valueInit(self) -> None:
        self.v6First = False
        self.count = 4
        self.timeout = 3

    def __valueCheck(self) -> None:  # check parameter values
        checker('TCPing', self.rules,
            self.server, self.port, self.v6First, self.count, self.timeout
        )

    def __valueDump(self) -> None:  # output parameter values
        logger.debug('[%s] TCPing server -> %s' % (self.id, self.server))
        logger.debug('[%s] TCPing port -> %d' % (self.id, self.port))
        logger.debug('[%s] TCPing v6First -> %s' % (self.id, self.v6First))
        logger.debug('[%s] TCPing count -> %d' % (self.id, self.count))
        logger.debug('[%s] TCPing timeout -> %d' % (self.id, self.timeout))

    def __runTcping(self) -> str:  # get raw output of tcping command
        tcpingCmd = [
            'tcping', self.server, str(self.port),
            '--counter', str(self.count),
            '--timeout', '%ds' % self.timeout
        ]
        logger.debug('[%s] TCPing command -> %s' % (self.id, tcpingCmd))
        process = runProcess(tcpingCmd)
        process.wait()  # wait ping process exit
        output = process.stdout.read().decode()
        logger.debug('[%s] TCPing raw output ->\n%s' % (self.id, output))
        return output

    def __init__(self, server: str, port: int) -> None:
        self.id = genFlag()
        self.__valueInit()
        self.server = server  # load ping server
        self.port = port # load tcping port
        logger.debug('[%s] TCPing task init -> %s(:%d)' % (self.id, self.server, self.port))

    def run(self) -> dict:
        self.__valueCheck()
        self.server = host2IP(self.server, self.v6First)  # convert into ip address
        logger.info('[%s] TCPing task -> %s(:%d)' % (self.id, self.server, self.port))
        self.__valueDump()

        result = self.__runTcping()

        # TODO: analyse tcping output

        logger.info('[%s] Ping result -> %s' % (self.id, result))
        return result
