#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from utils import logger
from utils import isHost
from utils import isPort
from utils import getAvg
from utils import getMin
from utils import getMax
from utils import checker
from utils import host2IP
from utils import genFlag
from utils import runProcess


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
    server = None  # load default values
    port = None
    host = None
    v6First = False
    verify = True
    count = 4

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
        tlspingCmd = ['tlsping', '-json', '-c', str(self.count)]
        if self.host != '':
            tlspingCmd += ['-host', self.host]
        if not self.verify:
            tlspingCmd += ['-insecure']
        tlspingCmd += ['%s:%d' % (self.server, self.port)]
        logger.debug('[%s] TLSPing command -> %s' % (self.id, tlspingCmd))
        process = runProcess(self.id, tlspingCmd, None)
        process.wait()  # wait tlsping process exit
        output = process.stdout.read().decode()
        logger.debug('[%s] TLSPing raw output ->\n%s' % (self.id, output))
        return output

    def __analyse(self, raw: str) -> dict:  # analyse tlsping output
        try:
            raw = json.loads(raw)
        except:
            return {
                'ip': self.server,  # actual address
                'port': self.port,
                'host': self.host,
                'alive': False,  # server offline
            }
        rawResult = [float('%.3f' % x) for x in raw['raw']]
        return {
            'ip': self.server,  # actual address
            'port': self.port,
            'host': self.host,
            'alive': True,  # server online
            'result': {
                'raw': rawResult,  # raw latency result
                'count': int(raw['count']),  # number of transmit tcping
                'avg': '%.3f' % getAvg(rawResult),  # average latency
                'min': '%.3f' % getMin(rawResult),  # minimum latency
                'max': '%.3f' % getMax(rawResult),  # maximum latency
                # TODO: add result statistic -> cv ...
                # 'sd': format(float(output['stddev']) * 1000, '.3f')
            }
        }

    def __init__(self, server: str, port: int) -> None:
        self.id = genFlag()
        self.server = server  # load tlsping server
        self.port = port # load tlsping port
        logger.debug('[%s] TLSPing task init -> %s(:%d)' % (self.id, self.server, self.port))

    def run(self) -> dict:
        if self.host is None:  # without host field
            self.host = self.server
        self.__valueCheck()
        request = {
            'server': self.server,
            'port': self.port,
            'host': self.host,
            'v6First': self.v6First,
            'verify': self.verify,
            'count': self.count,
        }
        self.server = host2IP(self.server, self.v6First)  # convert into ip address
        logger.info('[%s] TLSPing task -> %s(:%d)[%s]' % (self.id, self.server, self.port, self.host))
        self.__valueDump()
        result = {
            'request': request,
            **self.__analyse(self.__runTlsping()),
        }
        logger.info('[%s] TLSPing result -> %s' % (self.id, result))
        return result
