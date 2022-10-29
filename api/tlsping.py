#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from utils import logger
from flask import Response
from tlsping import TLSPing
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
    host = getArgument('host', str)
    v6First = getArgument('v6First', bool)
    verify = getArgument('verify', bool)
    count = getArgument('count', int)
    if host is not None: tlsping.host = host
    if v6First is not None: tlsping.v6First = v6First
    if verify is not None: tlsping.verify = verify
    if count is not None: tlsping.count = count
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
