#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from mtr import MTR
from utils import logger
from flask import Response
from api.utils import webApi
from api.utils import tokenCheck
from api.utils import getArgument
from api.utils import jsonResponse


def mtrMethod() -> dict:
    if not tokenCheck():
        raise RuntimeError('Invalid token')
    server = getArgument('server', str)
    if server is None:
        raise RuntimeError('Missing `server` option')
    mtr = MTR(server)
    v6First = getArgument('v6First', bool)
    if v6First is not None: mtr.v6First = v6First
    return mtr.run()


@webApi.route('/mtr', methods = ['GET', 'POST'])
def apiMTR() -> Response:
    try:
        return jsonResponse({
            'success': True,
            **mtrMethod(),
        })
    except Exception as exp:
        logger.error('MTR request error -> %s' % exp)
        return jsonResponse({
            'success': False,
            'message': str(exp),
        })
