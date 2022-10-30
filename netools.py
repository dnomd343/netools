#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import _thread
import logging
import argparse
import compileall
from utils import logger
from utils import constant
from api import startServer


def pythonCompile(dirRange: str = '/') -> None:  # python optimize compile
    for optimize in [-1, 1, 2]:
        compileall.compile_dir(dirRange, quiet = 1, optimize = optimize)
        logger.info('Python optimize compile -> %s (level = %i)' % (dirRange, optimize))


def parseArgs(rawArgs: list) -> argparse.Namespace:  # parse input arguments
    mainParser = argparse.ArgumentParser(description = 'Start running netools API server')
    mainParser.add_argument('-v', '--version', help = 'show version info and exit', action = 'store_true')
    mainParser.add_argument('--token', type = str, default = constant.ApiToken, help = 'api server verify token')
    mainParser.add_argument('--port', type = int, default = constant.ApiPort, help = 'api server listen port')
    mainParser.add_argument('--debug', help = 'enable debug mode', action = 'store_true')
    return mainParser.parse_args(rawArgs)


def loadArgs() -> None:  # load input arguments
    netoolsArgs = parseArgs(sys.argv[1:])
    if netoolsArgs.version:  # output version and exit
        print('ProxyC version %s' % constant.Version)
        sys.exit(0)
    if netoolsArgs.debug:  # enable debug level logging
        stdHandler = logger.handlers[0]
        stdHandler.setLevel(logging.DEBUG)
        logger.debug('Netools enable debug mode')
    constant.ApiPort = netoolsArgs.port  # load api port
    constant.ApiToken = netoolsArgs.token  # load api token


if __name__ == '__main__':
    loadArgs()  # load input arguments
    logger.warning('Netools starts running (%s)' % constant.Version)
    _thread.start_new_thread(
        pythonCompile, ('/usr',)  # python compile (generate .pyc file)
    )
    startServer(constant.ApiPort)  # start api server
