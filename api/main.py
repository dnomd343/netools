#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from utils import logger
from gevent import pywsgi
from api.utils import tokenCheck
from utils.constant import Version
from utils.constant import ApiToken
from flask import Flask, Response, request

webApi = Flask(__name__)  # init flask server


def jsonResponse(data: dict) -> Response:  # return json mime
    return Response(json.dumps(data), mimetype = 'application/json')


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


def startServer(apiPort: int) -> None:
    logger.warning('API server at http://:%i/' % apiPort)
    logger.warning('API ' + ('without token' if ApiToken == '' else 'token -> `%s`' % ApiToken))
    pywsgi.WSGIServer(('0.0.0.0', apiPort), webApi).serve_forever()  # powered by gevent
