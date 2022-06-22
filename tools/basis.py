#!/usr/bin/python3
# -*- coding:utf-8 -*-

import IPy
from dns import resolver


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


def v4Resolve(domain: str) -> list:
    result = []
    try:
        for ipAddr in resolver.resolve(domain, rdtype = 'A'):
            result.append(ipAddr.to_text())
        return sorted(result, key = lambda x: IPy.IP(x).int())
    except:  # resolve error
        return []


def v6Resolve(domain: str) -> list:
    result = []
    try:
        for ipAddr in resolver.resolve(domain, rdtype = 'AAAA'):
            result.append(ipAddr.to_text())
        return sorted(result, key = lambda x: IPy.IP(x).int())
    except:  # resolve error
        return []


def dnsResolve(domain: str) -> list:
    return v4Resolve(domain) + v6Resolve(domain)


def isIPv4(ipAddr: str) -> bool:
    try:
        if '/' in ipAddr: return False
        return IPy.IP(ipAddr).version() == 4
    except:
        pass
    return False


def isIPv6(ipAddr: str) -> bool:
    try:
        if '/' in ipAddr: return False
        return IPy.IP(ipAddr).version() == 6
    except:
        pass
    return False


def ipFormat(ipAddr: str) -> str:
    return str(IPy.IP(ipAddr))
