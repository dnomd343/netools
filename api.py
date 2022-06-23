#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json
from tools import *
from flask import Flask, Response, request

apiPath = '/'
api = Flask(__name__)


def httpPostArg(field: str) -> dict or str or None: # get HTTP POST param
    try:
        if request.values.get(field) is not None: # application/x-www-form-urlencoded
            return request.values.get(field)
        elif request.json.get(field) is not None: # application/json
            return request.json.get(field)
        elif request.form.get(field) is not None: # multipart/form-data
            return request.form.get(field)
    except:
        pass
    return None


def httpArgument(args: list) -> dict:
    result = {}
    for arg in args:
        if request.method == 'GET':
            result[arg] = request.args.get(arg)
        elif request.method == 'POST':
            result[arg] = httpPostArg(arg)
    return result


def responseJson(data: dict) -> Response:
    return Response(json.dumps(data), mimetype = 'application/json')


def toInt(raw) -> int or None:  # change to int
    if raw is None:
        return None
    if isinstance(raw, (int, float)): # int / float -> int
        return int(raw)
    elif isinstance(raw, bytes): # bytes -> str
        raw = str(raw, encoding = 'utf-8')
    elif not isinstance(raw, str):
        raise Exception('type not allowed')
    try:
        return int(raw)
    except:
        raise Exception('not a integer')


def toBool(raw) -> bool or None:  # change to bool
    if raw is None:
        return None
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, int):
        raw = str(raw)
    elif isinstance(raw, bytes):
        raw = str(raw, encoding = 'utf-8')
    elif not isinstance(raw, str):
        raise Exception('type not allowed')
    raw = raw.strip().lower()
    if raw == 'true':
        return True
    elif raw == 'false':
        return False
    else:
        try:
            raw = int(raw)
            return raw != 0
        except:
            raise Exception('not a boolean')


@api.route(apiPath + '/ping', methods = ['GET', 'POST'])
def pingMethod() -> Response:
    args = httpArgument(['server', 'v6First', 'count', 'fast', 'size', 'timeout'])
    try:
        return responseJson({
            'success': True,
            **ping.ping(args['server'], toBool(args['v6First']), toInt(args['count']),
                        toBool(args['fast']), toInt(args['size']), toInt(args['timeout']))
        })
    except Exception as exp:
        return responseJson({
            'success': False,
            'message': str(exp)
        })


@api.route(apiPath + '/tcping', methods = ['GET', 'POST'])
def tcpingMethod() -> Response:
    args = httpArgument(['server', 'port', 'v6First', 'count', 'timeout'])
    try:
        return responseJson({
            'success': True,
            **tcping.tcping(args['server'], toInt(args['port']), toBool(args['v6First']),
                            toInt(args['count']), toInt(args['timeout']))
        })
    except Exception as exp:
        return responseJson({
            'success': False,
            'message': str(exp)
        })

@api.route(apiPath + '/tlsping', methods = ['GET', 'POST'])
def tlspingMethod() -> Response:
    args = httpArgument(['server', 'port', 'host', 'v6First', 'count'])
    try:
        return responseJson({
            'success': True,
            **tlsping.tlsping(args['server'], toInt(args['port']), args['host'],
                              toBool(args['v6First']), toInt(args['count']))
        })
    except Exception as exp:
        return responseJson({
            'success': False,
            'message': str(exp)
        })

api.run(host = '0.0.0.0', port = 80, debug = True)
