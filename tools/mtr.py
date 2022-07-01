#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json
from tools import basis

def mtrProcess(server: str) -> dict:
    mtrCmd = ['mtr', '--no-dns', '--json', server]
    process = basis.startProcess(mtrCmd)
    process.wait()
    return json.loads(process.stdout.read().decode())['report']


def mtr(server: str, v6First: bool or None) -> dict:
    if server is None:
        raise RuntimeError('`server` cannot be None')
    server = basis.address2IP(server, v6First)

    try:
        return {
            'ip': server,  # actual address
            'result': mtrProcess(server)['hubs']
        }
    except Exception as exp:
        raise RuntimeError('unexpected error: ' + str(exp))
