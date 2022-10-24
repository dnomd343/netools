#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils import logger
from tcping import TCPing
from flask import Response
from api.utils import webApi
from api.utils import tokenCheck
from api.utils import getArgument
from api.utils import httpArgument
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

    # TODO: enhance fill process
    # if getArgument('v6First', bool) is not None:
    #     tcping.v6First = getArgument('v6First', bool)
    #
    # if getArgument('count', int) is not None:
    #     tcping.count = getArgument('count', int)
    #
    # if getArgument('fast', bool) is not None:
    #     tcping.fast = getArgument('fast', bool)
    #
    # if getArgument('size', bool) is not None:
    #     tcping.size = getArgument('size', bool)
    #
    # if getArgument('timeout', int) is not None:
    #     tcping.timeout = getArgument('timeout', int)

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
