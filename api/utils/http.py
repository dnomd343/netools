#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from utils import logger
from utils import typeStr
from flask import request
from flask import Response
from utils import toInt
from utils import toBool


def jsonResponse(data: dict) -> Response:  # return json mime
    return Response(json.dumps(data), mimetype = 'application/json')


def httpPostArg(field: str) -> str or None: # get HTTP POST param
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


def httpArgument(field: str) -> str or None:
    if request.method == 'GET':
        return request.args.get(field)
    elif request.method == 'POST':
        return httpPostArg(field)


def getArgument(field: str, fieldType: type):  # file argument from http request
    arg = httpArgument(field)
    if arg is None:  # field not exist
        return None
    if fieldType == int:
        arg = toInt(field, arg)
    elif fieldType == bool:
        arg = toBool(field, arg)
    logger.debug('Get Argument `%s` type `%s` -> `%s`' % (field, typeStr(fieldType), arg))
    return arg
