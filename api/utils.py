#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask import Flask
from flask import request
from flask import Response
from utils.constant import ApiToken

webApi = Flask(__name__)  # init flask server


def jsonResponse(data: dict) -> Response:  # return json mime
    return Response(json.dumps(data), mimetype = 'application/json')


def httpPostArg(field: str) -> dict or str or None: # get HTTP POST param
    try:
        if request.values.get(field) is not None: # application/x-www-form-urlencoded
            return request.values.get(field)
        elif request.json.get(field) is not None: # application/json
            return request.json.get(field)
        elif request.form.get(field) is not None: # multipart/form-data
            return request.form.get(field)
        else:
            return None
    except:
        return None


def httpArgument(args: list) -> dict:
    result = {}
    for arg in args:
        if request.method == 'GET':
            result[arg] = request.args.get(arg)
        elif request.method == 'POST':
            result[arg] = httpPostArg(arg)
    return result


def tokenCheck() -> bool:
    if ApiToken == '':  # token no need
        return True
    clientToken = httpArgument(['token'])['token']
    if clientToken is None or clientToken != ApiToken:  # invalid token
        return False
    return True


def toInt(prefix: str, raw) -> int:  # convert to int
    if isinstance(raw, (int, float)):  # int / float -> int
        return int(raw)
    elif isinstance(raw, bytes):  # bytes -> str
        raw = str(raw, encoding = 'utf-8')
    elif not isinstance(raw, str):
        raise RuntimeError('Field `%s` type not allowed' % prefix)
    try:
        return int(raw)
    except:
        raise RuntimeError('Field `%s` not a integer' % prefix)


def toBool(prefix: str, raw) -> bool:  # convert to bool
    if isinstance(raw, bool):  # bool -> bool
        return raw
    if isinstance(raw, int):  # int -> str
        raw = str(raw)
    elif isinstance(raw, bytes):  # bytes -> str
        raw = str(raw, encoding = 'utf-8')
    elif not isinstance(raw, str):
        raise RuntimeError('Field `%s` type not allowed' % prefix)
    raw = raw.strip().lower()
    if raw == 'true':
        return True
    elif raw == 'false':
        return False
    try:
        raw = int(raw)
        return raw != 0
    except:
        raise RuntimeError('Field `%s` not a boolean' % prefix)
