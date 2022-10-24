#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import logger
from api import startServer
from utils.constant import ApiPort
from utils.constant import Version

# TODO: add python compile

if __name__ == '__main__':
    logger.warning('Netools starts running (%s)' % Version)
    # _thread.start_new_thread(pythonCompile, ('/usr',))  # python compile (generate .pyc file)
    startServer(ApiPort)  # start api server
