#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

ApiPort = 5633
# TODO: remove default token before release
ApiToken = 'dnomd343'
Version = '0.9.1-dev'

environ = {x.lower(): os.environ[x] for x in os.environ}

if 'port' in environ:  # load port option from env
    ApiPort = environ['port']
if 'token' in environ:  # load token option from env
    ApiToken = environ['token']
