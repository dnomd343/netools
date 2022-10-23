#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import ctypes
import signal
import subprocess
from utils import logger

libcSysPaths = [
    '/usr/lib/libc.so.6',  # CentOS
    '/usr/lib64/libc.so.6',
    '/lib/libc.musl-i386.so.1',  # Alpine
    '/lib/libc.musl-x86_64.so.1',
    '/lib/libc.musl-aarch64.so.1',
    '/lib/i386-linux-gnu/libc.so.6',  # Debian / Ubuntu
    '/lib/x86_64-linux-gnu/libc.so.6',
    '/lib/aarch64-linux-gnu/libc.so.6',
]

libcPath = None
for path in libcSysPaths:
    if os.path.exists(path):  # try to locate libc.so
        libcPath = path
        break
if libcPath is None:  # lost libc.so -> unable to utilize prctl
    logger.warning('Dynamic link library `libc.so` not found')
else:
    logger.info('Dynamic link library `libc.so` located -> %s' % libcPath)


def runProcess(taskFlag: str, command: list, envVar: dict or None):  # running sub-process
    try:
        process = subprocess.Popen(  # start sub-process
            command,
            env = envVar,  # default with None
            stdout = subprocess.PIPE,  # fetch stdout output
            stderr = subprocess.DEVNULL,  # ignore stderr output
            preexec_fn = lambda: ctypes.CDLL(libcPath).prctl(1, signal.SIGTERM)  # avoid zombie process
        )
        logger.debug('[%s] Process `%s` start -> PID = %d' % (taskFlag, command[0], process.pid))
        return process
    except Exception as exp:
        logger.error('Process %s -> %s' % (command, exp))
        raise RuntimeError('Inner process error')
