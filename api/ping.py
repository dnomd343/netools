#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Response
from api.utils import webApi
from api.utils import tokenCheck
from api.utils import jsonResponse


def pingMethod() -> dict:
    if not tokenCheck():
        raise RuntimeError('Invalid token')
    return {
        'test': 'ok'
    }


@webApi.route('/ping', methods = ['GET', 'POST'])
def apiPing() -> Response:
    try:
        return jsonResponse({
            'success': True,
            **pingMethod(),
        })
    except Exception as exp:
        return jsonResponse({
            'success': False,
            'message': str(exp),
        })
    # args = httpArgument(['server', 'v6First', 'count', 'fast', 'size', 'timeout'])
    # try:
    #     return responseJson({
    #         'success': True,
    #         **ping.ping(args['server'], toBool(args['v6First']), toInt(args['count']),
    #                     toBool(args['fast']), toInt(args['size']), toInt(args['timeout']))
    #     })
    # except Exception as exp:
    #     return responseJson({
    #         'success': False,
    #         'message': str(exp)
    #     })

