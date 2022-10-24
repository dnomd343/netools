#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ping import Ping
from utils import logger
from flask import Response
from api.utils import webApi
from api.utils import tokenCheck
from api.utils import httpArgument
from api.utils import jsonResponse
from api.utils import toInt, toBool


def pingMethod() -> dict:
    if not tokenCheck():
        raise RuntimeError('Invalid token')
    server = httpArgument('server')
    if server is None:
        raise RuntimeError('Missing `server` option')
    ping = Ping(server)

    # TODO: combine check args process

    # if pingArgs['v6First'] is not None:
    #     ping.v6First = toBool('v6First', pingArgs['v6First'])
    # if pingArgs['count'] is not None:
    #     ping.count = toInt('count', pingArgs['count'])
    # if pingArgs['fast'] is not None:
    #     ping.fast = toBool('fast', pingArgs['fast'])
    # if pingArgs['size'] is not None:
    #     ping.size = toBool('size', pingArgs['size'])
    # if pingArgs['timeout'] is not None:
    #     ping.timeout = toInt('timeout', pingArgs['timeout'])

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
