#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json
from tools import basis


def tlspingProcess(server: str, port: int, host: str, count: int) -> str:
    tlspingCmd = ['tlsping', '-json', '-c', str(count)] + \
                 ([] if host == '' else ['-host', host]) + [server + ":" + str(port)]
    process = basis.startProcess(tlspingCmd)
    process.wait()
    return process.stdout.read().decode()


def tlsping(server: str, port: int, host: str or None, v6First: bool or None, count: int or None) -> dict:
    if server is None:
        raise RuntimeError('`server` cannot be None')
    if host is None: host = ''
    if not (basis.isIPv4(server) or basis.isIPv6(server)):  # server -> domain
        if host == '': host = server  # host not specified -> use server as sni
    server = basis.address2IP(server, v6First)

    if type(port) != int:
        raise RuntimeError('invalid `port` value')
    if port < 1 or port > 65535:  # port between 1 ~ 65535
        raise RuntimeError('`port` value out of range')

    if count is None: count = 4  # default times of ping
    if type(count) != int:
        raise RuntimeError('invalid `count` value')
    if count < 1 or count > 16:  # count between 1 ~ 16
        raise RuntimeError('`count` value out of range')

    result = {
        'ip': server,
        'port': port,
        'host': host,
        'times': count
    }
    rawOutput = tlspingProcess(server, port, host, count)
    try:
        output = json.loads(rawOutput)
    except:
        return {**result, 'alive': False}
    return {
        **result,
        'count': output['count'],
        'avg': format(output['average'], '.3f'),
        'min': format(output['min'], '.3f'),
        'max': format(output['max'], '.3f'),
        'stddev': format(output['stddev'], '.3f')
    }
