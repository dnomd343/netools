#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: load options from env vars and start params

import os

Version = '0.0.9'

ApiPort = 5633
ApiToken = 'dnomd343'
if 'token' in os.environ:
    ApiToken = os.environ['token']

LogLevel = 'debug'
LogFile = 'runtime.log'
