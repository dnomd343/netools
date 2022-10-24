#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request
from utils.constant import ApiToken


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
