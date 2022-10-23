#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
from utils import logger


def genFlag(length: int = 12) -> str:
    flag = ''
    for i in range(0, length):
        tmp = random.randint(0, 15)
        if tmp >= 10:
            flag += chr(tmp + 87)  # a ~ f
        else:
            flag += str(tmp)  # 0 ~ 9
    logger.debug('Generate new flag -> %s' % flag)
    return flag
