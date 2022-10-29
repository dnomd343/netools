#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.constant import ApiToken
from api.utils.http import httpArgument


def tokenCheck() -> bool:
    if ApiToken == '':  # token no need
        return True
    token = httpArgument('token')
    if token is None or token != ApiToken:  # invalid token
        return False
    return True
