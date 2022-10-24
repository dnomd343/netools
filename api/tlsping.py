#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from tlsping import TLSPing

from utils import logger
from flask import Response
from api.utils import webApi
from api.utils import tokenCheck
from api.utils import getArgument
from api.utils import jsonResponse


def tlspingMethod() -> dict:
    if not tokenCheck():
        raise RuntimeError('Invalid token')
    server = getArgument('server', str)
    port = getArgument('port', int)
    if server is None:
        raise RuntimeError('Missing `server` option')
    if port is None:
        raise RuntimeError('Missing `port` option')

    tlsping = TLSPing(server, port)

    if getArgument('host', str) is not None:
        tlsping.host = getArgument('host', str)

    # TODO: enhance fill process
    # if getArgument('v6First', bool) is not None:
    #     tlsping.v6First = getArgument('v6First', bool)
    #
    # if getArgument('count', int) is not None:
    #     tlsping.count = getArgument('count', int)
    #
    # if getArgument('fast', bool) is not None:
    #     tlsping.fast = getArgument('fast', bool)
    #
    # if getArgument('size', bool) is not None:
    #     tlsping.size = getArgument('size', bool)
    #
    # if getArgument('timeout', int) is not None:
    #     tlsping.timeout = getArgument('timeout', int)

    return tlsping.run()


@webApi.route('/tlsping', methods = ['GET', 'POST'])
def apiTLSPing() -> Response:
    try:
        return jsonResponse({
            'success': True,
            **tlspingMethod(),
        })
    except Exception as exp:
        logger.error('TLSPing request error -> %s' % exp)
        return jsonResponse({
            'success': False,
            'message': str(exp),
        })
