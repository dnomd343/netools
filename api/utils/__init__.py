#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from api.utils.token import tokenCheck
from api.utils.http import getArgument
from api.utils.http import httpArgument
from api.utils.http import jsonResponse

webApi = Flask(__name__)  # init flask server
