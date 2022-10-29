#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def getAvg(raw: list) -> float:
    valSum = 0
    for val in raw:
        valSum += val
    return valSum / len(raw)
