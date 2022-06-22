#!/usr/bin/python3
# -*- coding:utf-8 -*-

def getAverage(arrange: list) -> float:
    arrange = [float(x) for x in arrange]  # change into float list
    return sum(arrange) / len(arrange)


def getVariance(arrange: list, avg: float or None = None) -> float:
    arrange = [float(x) for x in arrange]  # change into float list
    if avg is None:
        avg = getAverage(arrange)  # calculate the average
    variance = 0
    for num in arrange:
        variance += (num - avg) ** 2
    return variance / (len(arrange) - 1)


def getCV(arrange: list, avg: float or None = None, variance: float or None = None) -> float:
    arrange = [float(x) for x in arrange]  # change into float list
    if avg is None:
        avg = getAverage(arrange)  # calculate the average
    if variance is None:
        variance = getVariance(arrange, avg)  # calculate the variance
    return variance ** 0.5 / avg  # calculate the coefficient of variation


def getArrangeInfo(arrange: list, isVariance: bool = False) -> dict:
    avg = getAverage(arrange)
    variance = getVariance(arrange, avg)
    info = {
        'avg': format(avg, '.3f'),
        'cv': format(getCV(arrange, avg, variance), '.3f')
    }
    if isVariance:
        info['var'] = format(variance, '.3f')
    return info
