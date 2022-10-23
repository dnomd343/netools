#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils import logger
from utils import checker
from utils import genFlag
from utils import host2IP
from utils import runProcess
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

    def __runTlsping(self) -> str:  # get raw output of tlsping command
        tlspingCmd = ['tlsping', '-json', '-c', str(self.count)]
        if self.host != '':
            tlspingCmd += ['-host', self.host]
        if not self.verify:
            tlspingCmd += ['-insecure']
        tlspingCmd += ['%s:%d' % (self.server, self.port)]
        logger.debug('[%s] TCPing command -> %s' % (self.id, tlspingCmd))
        process = runProcess(self.id, tlspingCmd, None)
        process.wait()  # wait ping process exit
        output = process.stdout.read().decode()
        logger.debug('[%s] TlsPing raw output ->\n%s' % (self.id, output))
        return output

    def __init__(self, server: str, port: int) -> None:
        self.id = genFlag()
        self.__valueInit()
        self.server = server  # load ping server
        self.port = port # load tcping port
        logger.debug('[%s] TlsPing task init -> %s(:%d)' % (self.id, self.server, self.port))

    def run(self) -> dict:
        self.__valueCheck()
        # TODO: fix host specify
        if self.host == '':  # without host field
            self.host = self.server
        self.server = host2IP(self.server, self.v6First)  # convert into ip address
        logger.info('[%s] TlsPing task -> %s(:%d)%s' % (self.id, self.server, self.port, ''))
        self.__valueDump()

        self.__runTlsping()


        # result = self.__analyse(self.__runTcping())
        # logger.info('[%s] TlsPing result -> %s' % (self.id, result))
        # return result
        return {}
