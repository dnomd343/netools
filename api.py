#!/usr/bin/python3
# -*- coding:utf-8 -*-

from tools import *
from flask import Flask, request

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


@api.route(apiPath + '/ping', methods = ['GET', 'POST'])
def pingMethod() -> dict:
    if request.method == 'GET':
        # try:
            return {
                'success': True,
                **ping.ping(
                    request.args.get('server'),
                    request.args.get('v6First'),
                    request.args.get('count'),
                    request.args.get('fast'),
                    request.args.get('size'),
                    request.args.get('timeout'),
                )
            }
        # except:
        #     pass
    elif request.method == 'POST':
        pass


api.run(host = '0.0.0.0', port = 80, debug = True)
