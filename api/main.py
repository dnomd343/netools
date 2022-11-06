#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import logger
from gevent import pywsgi
from flask import Response
from api.utils import webApi
from api.utils import tokenCheck
from api.utils import jsonResponse
from utils.constant import Version
from utils.constant import ApiToken


@webApi.route('/token', methods = ['GET'])
def checkToken() -> Response:
    tokenStatus = tokenCheck()
    logger.debug('API check token -> %s' % tokenStatus)
    return jsonResponse({
        'success': True,
        'token': tokenStatus,
    })


@webApi.route('/version', methods = ['GET'])
def getVersion() -> Response:
    logger.debug('API get version -> %s' % Version)
    return jsonResponse({
        'success': True,
        'version': Version,
    })


def startServer(apiPort: int, devMode: bool = False) -> None:
    logger.warning('API server at http://:%i/' % apiPort)
    logger.warning('API ' + ('without token' if ApiToken == '' else 'token -> `%s`' % ApiToken))
    if devMode:
        webApi.run(host = '0.0.0.0', port = apiPort, debug = True, threaded = True)
    else:
        pywsgi.WSGIServer(('0.0.0.0', apiPort), webApi).serve_forever()  # powered by gevent
