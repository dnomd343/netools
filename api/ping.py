#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ping import Ping
from utils import logger
from flask import Response
from api.utils import webApi
from api.utils import tokenCheck
from api.utils import getArgument
from api.utils import httpArgument
from api.utils import jsonResponse


def pingMethod() -> dict:
    if not tokenCheck():
        raise RuntimeError('Invalid token')
    server = httpArgument('server')
    if server is None:
        raise RuntimeError('Missing `server` option')
    ping = Ping(server)

    # TODO: enhance fill process
    if getArgument('v6First', bool) is not None:
        ping.v6First = getArgument('v6First', bool)

    if getArgument('count', int) is not None:
        ping.count = getArgument('count', int)

    if getArgument('fast', bool) is not None:
        ping.fast = getArgument('fast', bool)

    if getArgument('size', bool) is not None:
        ping.size = getArgument('size', bool)

    if getArgument('timeout', int) is not None:
        ping.timeout = getArgument('timeout', int)

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
