#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils import logger
from tcping import TCPing
from flask import Response
from api.utils import webApi
from api.utils import tokenCheck
from api.utils import getArgument
from api.utils import jsonResponse


def tcpingMethod() -> dict:
    if not tokenCheck():
        raise RuntimeError('Invalid token')
    server = getArgument('server', str)
    port = getArgument('port', int)
    if server is None:
        raise RuntimeError('Missing `server` option')
    if port is None:
        raise RuntimeError('Missing `port` option')
    tcping = TCPing(server, port)
    v6First = getArgument('v6First', bool)
    fast = getArgument('fast', bool)
    count = getArgument('count', int)
    timeout = getArgument('timeout', int)
    if v6First is not None: tcping.v6First = v6First
    if fast is not None: tcping.fast = fast
    if count is not None: tcping.count = count
    if timeout is not None: tcping.timeout = timeout
    return tcping.run()


@webApi.route('/tcping', methods = ['GET', 'POST'])
def apiTCPing() -> Response:
    try:
        return jsonResponse({
            'success': True,
            **tcpingMethod(),
        })
    except Exception as exp:
        logger.error('TCPing request error -> %s' % exp)
        return jsonResponse({
            'success': False,
            'message': str(exp),
        })
