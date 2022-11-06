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
    return variance / len(arrange)


def getCV(arrange: list, avg: float or None = None, variance: float or None = None) -> float:
    arrange = [float(x) for x in arrange]  # change into float list
    if avg is None:
        avg = getAverage(arrange)  # calculate the average
    if variance is None:
        variance = getVariance(arrange, avg)  # calculate the variance
    return variance ** 0.5 / avg  # calculate the coefficient of variation


def getArrangeInfo(arrange: list, isCV: bool = False) -> dict:
    arrange = [float(x) for x in arrange]  # change into float list
    avg = getAverage(arrange)
    variance = getVariance(arrange, avg)
    info = {
        'avg': format(avg, '.3f'),
        'min': format(min(arrange), '.3f'),
        'max': format(max(arrange), '.3f'),
        'sd': format(variance ** 0.5, '.3f'),
    }
    if isCV:
        info['cv'] = format(getCV(arrange, avg, variance), '.3f')
    return info
