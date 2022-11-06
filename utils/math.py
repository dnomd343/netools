#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def getAvg(raw: list) -> float:
    valSum = 0
    for val in raw:
        valSum += val
    return valSum / len(raw)


def getMin(raw: list) -> float:
    return min(raw)


def getMax(raw: list) -> float:
    return max(raw)


def resultAnalyse(raw: list) -> dict:
    return {
        'avg': '%.3f' % getAvg(raw),  # average latency
        'min': '%.3f' % getMin(raw),  # minimum latency
        'max': '%.3f' % getMax(raw),  # maximum latency
        # TODO: add cv / sd statistics ...
    }
