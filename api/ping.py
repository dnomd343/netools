#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ping import Ping
from utils import logger
from flask import Response
from api.utils import webApi
from api.utils import tokenCheck
from api.utils import getArgument
from api.utils import jsonResponse


def pingMethod() -> dict:
    if not tokenCheck():
        raise RuntimeError('Invalid token')
    server = getArgument('server', str)
    if server is None:
        raise RuntimeError('Missing `server` option')
    ping = Ping(server)
    v6First = getArgument('v6First', bool)
    count = getArgument('count', int)
    fast = getArgument('fast', bool)
    size = getArgument('size', int)
    timeout = getArgument('timeout', int)
    if v6First is not None: ping.v6First = v6First
    if count is not None: ping.count = count
    if fast is not None: ping.fast = fast
    if size is not None: ping.size = size
    if timeout is not None: ping.timeout = timeout
    return ping.run()


@webApi.route('/ping', methods = ['GET', 'POST'])
def apiPing() -> Response:
    try:
        return jsonResponse({
            'success': True,
            **pingMethod(),
        })
    except Exception as exp:
        logger.error('Ping request error -> %s' % exp)
        return jsonResponse({
            'success': False,
            'message': str(exp),
        })
