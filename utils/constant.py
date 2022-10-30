#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

Version = '0.9.0-dev'

ApiPort = 5633
ApiToken = 'dnomd343'

LogLevel = 'info'
LogFile = 'runtime.log'

# TODO: load options from env vars

if 'token' in os.environ:
    ApiToken = os.environ['token']
