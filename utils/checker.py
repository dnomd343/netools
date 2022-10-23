#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from utils import logger


def typeStr(t: type) -> str:  # get python type name
    match = re.search(r'^<class \'(\S+)\'>$', str(t))
    if match is not None:
        return match[1]  # <class 'xxx'>
    return 'unknown'


def checker(caption: str, rules: list, *args) -> None:
    if len(rules) != len(args):
        raise RuntimeError('Number of arguments incorrect')
    for i in range(0, len(args)):  # traverse all arguments
        argName = rules[i][0]
        argType = rules[i][1]
        argVerify = rules[i][2]
        if type(args[i]) != argType:  # argument type check
            errMsg = '%s option `%s` must be %s type' % (caption, argName, typeStr(argType))
            logger.debug('Checker error -> %s' % errMsg)
            raise RuntimeError(errMsg)
        if argVerify is None:  # skip check process
            continue
        if not argVerify(args[i]):  # run verify function
            errMsg = '%s option `%s` with invalid value `%s`' % (caption, argName, args[i])
            logger.debug('Checker error -> %s' % errMsg)
            raise RuntimeError(errMsg)
