#!/usr/bin/python3
# -*- coding:utf-8 -*-

import re
from tools import basis


def pingProcess(server: str, count: int, fast: bool, size: int, timeout: int) -> str:
    pingCmd = ['ping', server, '-c', str(count), '-s', str(size), '-w', str(timeout)]
    if fast:  # fast mode
        pingCmd.append('-A')
    process = basis.startProcess(pingCmd)
    process.wait()
    return process.stdout.read().decode()


def ping(server: str, v6First: bool or None, count: int or None,
         fast: bool or None, size: int or None, timeout: int or None) -> dict:
    if server is None:
        raise RuntimeError('`server` cannot be None')
    server = basis.address2IP(server, v6First)

    if count is None: count = 16  # default times of ping
    if type(count) != int:
        raise RuntimeError('invalid `count` value')
    if count < 1 or count > 64:  # count between 1 ~ 64
        raise RuntimeError('`count` value out of range')

    if fast is None: fast = True  # default use fast mode
    if type(fast) != bool:
        raise RuntimeError('invalid `fast` value')

    if size is None: size = 56  # default data bytes in packets
    if type(size) != int:
        raise RuntimeError('invalid `size` value')
    if size < 4 or size > 1016:  # size between 4 ~ 1016
        raise RuntimeError('`size` value out of range')

    if timeout is None: timeout = 20  # default wait for 20s
    if type(timeout) != int:
        raise RuntimeError('invalid `timeout` value')
    if timeout < 1 or timeout > 60:  # timeout between 1 ~ 60
        raise RuntimeError('`timeout` value out of range')

    sendTimes = 0
    ttlValue = []
    pingResult = []
    rawOutput = pingProcess(server, count, fast, size, timeout).split('\n')
    for i in range(1, len(rawOutput)):  # skip first line
        if rawOutput[i].strip() == '': continue
        if 'ping statistics' in rawOutput[i]:  # statistics info after this line
            sendTimes = re.search(r'(\d+) packets transmitted', rawOutput[i + 1])[1]
            break
        if 'bytes from' not in rawOutput[i]: continue
        ttlValue.append(int(re.search(r'ttl=(\d+)', rawOutput[i])[1]))
        pingResult.append(re.search(r'time=([\d.]+)', rawOutput[i])[1])
    if len(pingResult) == 0:
        return {'ip': server, 'alive': False}  # none returned

    return {
        'ip': server,  # actual address
        'alive': True,
        'ttl': max(ttlValue, key = ttlValue.count),  # element with the most occurrences
        'statistics': {
            'count': int(sendTimes),  # number of transmit pings
            'reply': len(pingResult),  # number of successful pings
            'rate': format(len(pingResult) / int(sendTimes) * 100, '.1f') + '%',  # success rate
            **basis.getArrangeInfo(pingResult)
        }
    }
