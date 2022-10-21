#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from utils import logger


def typeStr(t: type) -> str:
    match = re.search(r'^<class \'(\S+)\'>$', str(t))
    if match is not None:
        return match[1]
    return 'unknown'


def checker(caption: str, rules: list, *args) -> None:
    if len(rules) != len(args):
        raise RuntimeError('Args number error')

    for i in range(0, len(args)):
        if type(args[i]) != rules[i][1]:  # argument type check
            errMsg = '%s option `%s` must be %s type' % (
                caption, rules[i][0], typeStr(rules[i][1])
            )
            logger.warning(errMsg)
            raise RuntimeError(errMsg)
        # print(rules[i][1])


    # for i in range()

    # print(args[0])
    # print(len(args))



        # if type(self.v6First) != bool:
        #     logger.warning('Ping option `v6First` must be bool type')
        #     raise RuntimeError('`v6First` type error')
        #
        # if type(self.count) != int:
        #     logger.warning('Ping option `count` must be int type')
        #     raise RuntimeError('`count` type error')
        # if self.count < 1 or self.count > 64:  # count between 1 ~ 64
        #     raise RuntimeError('`count` out of range')
        #
        # if type(self.fast) != bool:
        #     logger.warning('Ping option `fast` must be bool type')
        #     raise RuntimeError('`fast` type error')
        #
        # if type(self.size) != int:
        #     logger.warning('Ping option `size` must be int type')
        #     raise RuntimeError('`size` type error')
        # if self.size < 4 or self.size > 1016:  # size between 4 ~ 1016
        #     raise RuntimeError('`size` out of range')
        #
        # if type(self.timeout) != int:
        #     raise RuntimeError('`timeout` type error')
        # if self.timeout < 1 or self.timeout > 60:  # timeout between 1 ~ 60
        #     raise RuntimeError('`timeout` out of range')
