#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import colorlog

logColor = {  # log color
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

dateFormat = '%Y-%m-%d %H:%M:%S'
timeFormat = '%(asctime)s.%(msecs)03d'
logFormat = '[%(levelname)s] %(message)s (%(module)s.%(funcName)s:%(lineno)d)'

# load fileHandler -> log file
fileHandler = logging.FileHandler('runtime.log', encoding = 'utf-8')
fileHandler.setFormatter(logging.Formatter(
    '[' + timeFormat + '] ' + logFormat,
    datefmt = dateFormat
))
fileHandler.setLevel(logging.DEBUG)  # debug level for log file

# load stdHandler -> stderr
stdHandler = colorlog.StreamHandler()
stdHandler.setFormatter(colorlog.ColoredFormatter(
    '%(light_black)s' + timeFormat + '%(log_color)s ' + logFormat,
    datefmt = dateFormat,
    log_colors = logColor,
    stream = sys.stderr
))
stdHandler.setLevel(logging.INFO)  # info level for stderr

logger = logging.getLogger()
logger.addHandler(stdHandler)
logger.addHandler(fileHandler)
logger.setLevel(logging.DEBUG)  # set log level in handler
