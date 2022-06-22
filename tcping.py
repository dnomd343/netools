#!/usr/bin/python3
# -*- coding:utf-8 -*-

import re
import math
import subprocess


def tcpingProcess(server: str, port: int, count: int, timeout: int) -> str:
    tcpingCmd = ['tcping', server, str(port), '--counter', str(count), '--timeout', str(timeout) + 's']
    process = subprocess.Popen(tcpingCmd, stdout = subprocess.PIPE, stderr = subprocess.DEVNULL)
    process.wait()
    return process.stdout.read().decode()


def tcping(server: str, port: int, v6First: bool or None, count: int or None, timeout: int or None) -> dict:

    # TODO: server is domain -> IP address (v4/v6)

    if type(port) != int:
        raise RuntimeError('invalid `port` value')
    if port < 1 or port > 65535:  # port between 1 ~ 65535
        raise RuntimeError('`port` value out of range')

    if count is None: count = 4  # default times of ping
    if type(count) != int:
        raise RuntimeError('invalid `count` value')
    if count < 1 or count > 16:  # count between 1 ~ 16
        raise RuntimeError('`count` value out of range')

    if timeout is None: timeout = 3  # default wait for 3s
    if type(timeout) != int:
        raise RuntimeError('invalid `timeout` value')
    if timeout < 1 or timeout > 10:  # timeout between 1 ~ 10
        raise RuntimeError('`timeout` value out of range')

    tcpingResult = []
    rawOutput = tcpingProcess(server, port, count, timeout).split('\n')
    for row in rawOutput:
        if row.strip() == '': break  # test complete
        if 'Connected' not in row: continue  # connect failed
        time = re.search(r'time=(\S+)', row)[1]
        if time.endswith('ms'):
            time = float(time[:-2])
        elif time.endswith('µs'):
            time = float(time[:-2]) / 1000
        elif time.endswith('s'):
            time = float(time[:-1]) * 1000
        else:  # others, skip it
            continue
        tcpingResult.append(time)
    if len(tcpingResult) == 0:
        return {'ip': server, 'times': 0, 'count': count}
    return {
        'ip': server,  # actual address
        'times': len(tcpingResult),  # number of successful tcpings
        'count': count,  # tried numbers
        **math.getArrangeInfo(tcpingResult),
        'value': [format(x, '.3f') for x in tcpingResult]
    }

ret = tcping('8.210.148.24', port = 80, v6First = None, count = 4, timeout = 2)
print(ret)
