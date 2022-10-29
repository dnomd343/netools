#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from utils import logger
from utils import isHost
from utils import isPort
from utils import getAvg
from utils import host2IP
from utils import checker
from utils import genFlag
from utils import runProcess


class TCPing:
    """Netools tcping module

    Attributes:
        server: TCPing package target. (ipv4 / ipv6 / domain)
        port: TCP port for connection. (1 ~ 65535)
        v6First: IPv6 is preferred. (server -> domain name)
        fast: TCPing as soon as reply is received.
        count: The number of tcp connection tried. (1 ~ 16)
        timeout: Time limit for each connection. (1 ~ 10)
    """
    rules = [  # parameter rules
        ('server', str, isHost),
        ('port', int, isPort),
        ('v6First', bool, None),
        ('fast', bool, None),
        ('count', int, lambda x: 1 <= x <= 16),
        ('timeout', int, lambda x: 1 <= x <= 10),
    ]
    server = None  # load default values
    port = None
    v6First = False
    fast = True
    count = 4
    timeout = 3

    def __valueCheck(self) -> None:  # check parameter values
        checker('TCPing', self.rules,
            self.server, self.port, self.v6First, self.fast, self.count, self.timeout
        )

    def __valueDump(self) -> None:  # output parameter values
        logger.debug('[%s] TCPing server -> %s' % (self.id, self.server))
        logger.debug('[%s] TCPing port -> %d' % (self.id, self.port))
        logger.debug('[%s] TCPing v6First -> %s' % (self.id, self.v6First))
        logger.debug('[%s] TCPing fast -> %s' % (self.id, self.fast))
        logger.debug('[%s] TCPing count -> %d' % (self.id, self.count))
        logger.debug('[%s] TCPing timeout -> %d' % (self.id, self.timeout))

    def __runTcping(self) -> str:  # get raw output of tcping command
        tcpingCmd = [
            'tcping', self.server, str(self.port),
            '--counter', str(self.count),
            '--timeout', '%ds' % self.timeout,
        ]
        if self.fast:  # enable fast mode
            tcpingCmd += ['--interval', '1ns']
        logger.debug('[%s] TCPing command -> %s' % (self.id, tcpingCmd))
        process = runProcess(self.id, tcpingCmd, None)
        process.wait()  # wait tcping process exit
        output = process.stdout.read().decode()
        logger.debug('[%s] TCPing raw output ->\n%s' % (self.id, output))
        return output

    def __analyse(self, raw: str) -> dict:  # analyse tcping output
        result = []
        for row in raw.split('\n'):
            if row.strip() == '':  # test complete
                break
            if 'connected' not in row:  # connect failed
                continue
            tcpingTime = re.search(r'time=(\S+)', row)[1]
            if tcpingTime.endswith('ms'):
                tcpingTime = float(tcpingTime[:-2])
            elif tcpingTime.endswith('µs'):
                tcpingTime = float(tcpingTime[:-2]) / 1000
            elif tcpingTime.endswith('s'):
                tcpingTime = float(tcpingTime[:-1]) * 1000
            else:  # skip others time format
                continue
            result.append(
                float('%.3f' % tcpingTime)
            )
        if len(result) == 0:
            return {
                'ip': self.server,  # actual address
                'port': self.port,
                'alive': False,  # server offline
            }
        return {
            'ip': self.server,  # actual address
            'port': self.port,
            'alive': True,  # server online
            'result': {
                'raw': result,  # raw latency result
                'count': self.count,  # number of transmit tcping
                'reply': len(result),  # number of successful tcping
                'rate': '%s%%' % format(len(result) / self.count * 100, '.1f'),  # success rate
                'avg': '%.3f' % getAvg(result),  # average latency
                # TODO: result analyse -> avg / cv ...
            }
        }

    def __init__(self, server: str, port: int) -> None:
        self.id = genFlag()
        self.server = server  # load tcping server
        self.port = port # load tcping port
        logger.debug('[%s] TCPing task init -> %s(:%d)' % (self.id, self.server, self.port))

    def run(self) -> dict:
        self.__valueCheck()
        request = {
            'server': self.server,
            'port': self.port,
            'v6First': self.v6First,
            'fast': self.fast,
            'count': self.count,
            'timeout': self.timeout,
        }
        self.server = host2IP(self.server, self.v6First)  # convert into ip address
        logger.info('[%s] TCPing task -> %s(:%d)' % (self.id, self.server, self.port))
        self.__valueDump()
        result = {
            'request': request,
            **self.__analyse(self.__runTcping()),
        }
        logger.info('[%s] TCPing result -> %s' % (self.id, result))
        return result
