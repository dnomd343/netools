#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import _thread
import compileall
from utils import logger
from api import startServer
from utils.constant import ApiPort
from utils.constant import Version


def pythonCompile(dirRange: str = '/') -> None:  # python optimize compile
    for optimize in [-1, 1, 2]:
        compileall.compile_dir(dirRange, quiet = 1, optimize = optimize)
        logger.info('Python optimize compile -> %s (level = %i)' % (dirRange, optimize))


if __name__ == '__main__':
    logger.warning('Netools starts running (%s)' % Version)
    _thread.start_new_thread(
        pythonCompile, ('/usr',)  # python compile (generate .pyc file)
    )
    startServer(ApiPort)  # start api server
