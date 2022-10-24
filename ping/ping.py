#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from utils import logger
from utils import isHost
from utils import checker
from utils import host2IP
from utils import genFlag
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
    rules = [  # parameter rules
        ('server', str, isHost),
        ('v6First', bool, None),
        ('count', int, lambda x: 1 <= x <= 64),
        ('fast', bool, None),
        ('size', int, lambda x: 4 <= x <= 1016),
        ('timeout', int, lambda x: 1 <= x <= 60),
    ]
    server = None  # load default values
    v6First = False
    count = 16
    fast = True
    size = 56
    timeout = 20

    def __valueCheck(self) -> None:  # check parameter values
        checker('Ping', self.rules,
            self.server, self.v6First, self.count, self.fast, self.size, self.timeout
        )

    def __valueDump(self) -> None:  # output parameter values
        logger.debug('[%s] Ping server -> %s' % (self.id, self.server))
        logger.debug('[%s] Ping v6First -> %s' % (self.id, self.v6First))
        logger.debug('[%s] Ping count -> %d' % (self.id, self.count))
        logger.debug('[%s] Ping fast -> %s' % (self.id, self.fast))
        logger.debug('[%s] Ping size -> %d' % (self.id, self.size))
        logger.debug('[%s] Ping timeout -> %d' % (self.id, self.timeout))

    def __runPing(self) -> str:  # get raw output of ping command
        pingCmd = [
            'ping', self.server,
            '-c', str(self.count),
            '-s', str(self.size),
            '-w', str(self.timeout),
        ]
        if self.fast:  # enabled fast mode
            pingCmd.append('-A')
        logger.debug('[%s] Ping command -> %s' % (self.id, pingCmd))
        process = runProcess(self.id, pingCmd, None)
        process.wait()  # wait ping process exit
        output = process.stdout.read().decode()
        logger.debug('[%s] Ping raw output ->\n%s' % (self.id, output))
        return output

    def __analyse(self, raw: str) -> dict:  # analyse ping output
        result = []
        sendTimes = 0
        raw = [x.strip() for x in raw.split('\n') if x.strip() != '']  # remove empty line
        for i in range(1, len(raw)):  # skip first line
            if 'ping statistics' in raw[i]:  # statistics info after this line
                sendTimes = re.search(r'(\d+) packets transmitted', raw[i + 1])[1]
                break  # exit match process
            if 'bytes from' not in raw[i]:  # ping failed
                continue
            result.append((
                int(re.search(r'ttl=(\d+)', raw[i])[1]),  # ttl value
                re.search(r'time=([\d.]+)', raw[i])[1], # ping value
            ))
        if len(result) == 0:  # without successful ping
            return {
                'ip': self.server,  # actual address
                'alive': False,  # server offline
            }
        ttlValue = [x[0] for x in result]
        return {
            'ip': self.server,  # actual address
            'alive': True,  # server online
            'ttl': max(ttlValue, key = ttlValue.count),  # element with the most occurrences
            'result': {
                'raw': [float(x[1]) for x in result],  # raw latency result
                'count': int(sendTimes),  # number of transmit ping
                'reply': len(result),  # number of successful ping
                'rate': '%s%%' % format(len(result) / int(sendTimes) * 100, '.1f'),  # success rate
                # TODO: add result statistic -> avg / cv ...
            }
        }

    def __init__(self, server: str) -> None:
        self.id = genFlag()
        self.server = server  # load ping target
        logger.debug('[%s] Ping task init -> %s' % (self.id, self.server))

    def run(self) -> dict:
        self.__valueCheck()
        request = {
            'server': self.server,
            'v6First': self.v6First,
            'count': self.count,
            'fast': self.fast,
            'size': self.size,
            'timeout': self.timeout,
        }
        self.server = host2IP(self.server, self.v6First)  # convert into ip address
        logger.info('[%s] Ping task -> %s' % (self.id, self.server))
        self.__valueDump()
        result = {
            'request': request,
            **self.__analyse(self.__runPing()),
        }
        logger.info('[%s] Ping result -> %s' % (self.id, result))
        return result
