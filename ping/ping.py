#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils import logger
from utils import checker

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
    def __valueInit(self) -> None:  # load default value
        self.server = ''
        self.v6First = False
        self.count = 16
        self.fast = True
        self.size = 56
        self.timeout = 20

    def __valueCheck(self) -> None:
        # TODO: server option check

        if type(self.v6First) != bool:
            logger.warning('Ping option `v6First` must be bool type')
            raise RuntimeError('`v6First` type error')

        if type(self.count) != int:
            logger.warning('Ping option `count` must be int type')
            raise RuntimeError('`count` type error')
        if self.count < 1 or self.count > 64:  # count between 1 ~ 64
            raise RuntimeError('`count` out of range')

        if type(self.fast) != bool:
            logger.warning('Ping option `fast` must be bool type')
            raise RuntimeError('`fast` type error')

        if type(self.size) != int:
            logger.warning('Ping option `size` must be int type')
            raise RuntimeError('`size` type error')
        if self.size < 4 or self.size > 1016:  # size between 4 ~ 1016
            raise RuntimeError('`size` out of range')

        if type(self.timeout) != int:
            raise RuntimeError('`timeout` type error')
        if self.timeout < 1 or self.timeout > 60:  # timeout between 1 ~ 60
            raise RuntimeError('`timeout` out of range')

        limit = dict(v6First = {
            'type': bool,
            'check': lambda x: True
        }, count = {
            'type': int,
            'check': lambda x: 1 <= x <= 64
        }, fast = {
            'type': bool,
            'check': lambda x: True
        })
        checker(limit, self.v6First, self.count, self.fast)

    def __init__(self, server: str) -> None:
        self.__valueInit()
        self.server = server

    def run(self):
        self.__valueCheck()
        # TODO: ping process
