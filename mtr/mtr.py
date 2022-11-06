#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from utils import logger
from utils import isHost
from utils import checker
from utils import host2IP
from utils import genFlag
from utils import runProcess


class MTR:
    """Netools mtr module

    Attributes:
        server: MTR package target. (ipv4 / ipv6 / domain)
        v6First: IPv6 is preferred. (server -> domain name)
    """
    rules = [  # parameter rules
        ('server', str, isHost),
        ('v6First', bool, None),
    ]
    server = None  # load default values
    v6First = False

    def __valueCheck(self) -> None:  # check parameter values
        checker('MTR', self.rules, self.server, self.v6First)

    def __valueDump(self) -> None:  # output parameter values
        logger.debug('[%s] MTR server -> %s' % (self.id, self.server))
        logger.debug('[%s] MTR v6First -> %s' % (self.id, self.v6First))

    def __runMtr(self) -> str:  # get raw output of mtr command
        mtrCmd = ['mtr', '--no-dns', '--json', self.server]
        logger.debug('[%s] MTR command -> %s' % (self.id, mtrCmd))
        process = runProcess(self.id, mtrCmd, None)
        process.wait()  # wait mtr process exit
        output = process.stdout.read().decode()
        logger.debug('[%s] MTR raw output ->\n%s' % (self.id, output))
        return output

    def __analyse(self, raw: str) -> dict:  # analyse mtr output
        return {
            'ip': self.server,  # actual address
            'result': json.loads(raw)
        }

    def __init__(self, server: str) -> None:
        self.id = genFlag()
        self.server = server  # load mtr server
        logger.debug('[%s] MTR task init -> %s' % (self.id, self.server))

    def run(self) -> dict:
        self.__valueCheck()
        request = {
            'server': self.server,
            'v6First': self.v6First,
        }
        self.server = host2IP(self.server, self.v6First)  # convert into ip address
        logger.info('[%s] MTR task -> %s' % (self.id, self.server))
        self.__valueDump()
        result = {
            'request': request,
            **self.__analyse(self.__runMtr()),
        }
        logger.info('[%s] MTR result -> %s' % (self.id, result))
        return result
