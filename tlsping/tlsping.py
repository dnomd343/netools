#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from utils import logger
from utils import checker
from utils import genFlag
from utils import host2IP
from utils import runProcess
from utils import isPort, isHost


class TLSPing:
    """Netools tlsping module

    Attributes:
        server: TLSPing package target. (ipv4 / ipv6 / domain)
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
        checker('TLSPing', self.rules,
            self.server, self.port, self.host, self.v6First, self.verify, self.count
        )

    def __valueDump(self) -> None:  # output parameter values
        logger.debug('[%s] TLSPing server -> %s' % (self.id, self.server))
        logger.debug('[%s] TLSPing port -> %d' % (self.id, self.port))
        logger.debug('[%s] TLSPing host -> %s' % (self.id, self.host))
        logger.debug('[%s] TLSPing v6First -> %s' % (self.id, self.v6First))
        logger.debug('[%s] TLSPing verify -> %s' % (self.id, self.verify))
        logger.debug('[%s] TLSPing count -> %d' % (self.id, self.count))

    def __runTlsping(self) -> str:  # get raw output of tlsping command
        # TODO: show each result
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
        logger.debug('[%s] TLSPing raw output ->\n%s' % (self.id, output))
        return output

    def __analyse(self, raw: str) -> dict:  # analyse tlsping output
        try:
            output = json.loads(raw)
        except:
            return {
                'ip': self.server,  # actual address
                'port': self.port,
                'host': self.host,
                'alive': False,  # server offline
            }
        return {
            'ip': self.server,  # actual address
            'port': self.port,
            'host': self.host,
            'alive': True,  # server online
            'statistics': {
                'count': int(output['count']),
                # TODO: analyse result
                # 'avg': format(float(output['average']) * 1000, '.3f'),
                # 'min': format(float(output['min']) * 1000, '.3f'),
                # 'max': format(float(output['max']) * 1000, '.3f'),
                # 'sd': format(float(output['stddev']) * 1000, '.3f')
            }
        }

    def __init__(self, server: str, port: int) -> None:
        self.id = genFlag()
        self.__valueInit()
        self.server = server  # load ping server
        self.port = port # load tcping port
        logger.debug('[%s] TLSPing task init -> %s(:%d)' % (self.id, self.server, self.port))

    def run(self) -> dict:
        self.__valueCheck()
        # TODO: fix host specify
        if self.host == '':  # without host field
            self.host = self.server
        self.server = host2IP(self.server, self.v6First)  # convert into ip address
        logger.info('[%s] TLSPing task -> %s(:%d)%s' % (self.id, self.server, self.port, ''))
        self.__valueDump()
        result = self.__analyse(self.__runTlsping())
        logger.info('[%s] TLSPing result -> %s' % (self.id, result))
        return result
