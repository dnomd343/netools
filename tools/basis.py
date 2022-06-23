#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import IPy
import ctypes
import signal
import subprocess
from dns import resolver

libcPaths = [
    '/usr/lib/libc.so.6', # CentOS
    '/usr/lib64/libc.so.6',
    '/lib/libc.musl-i386.so.1', # Alpine
    '/lib/libc.musl-x86_64.so.1',
    '/lib/libc.musl-aarch64.so.1',
    '/lib/i386-linux-gnu/libc.so.6', # Debian / Ubuntu
    '/lib/x86_64-linux-gnu/libc.so.6',
    '/lib/aarch64-linux-gnu/libc.so.6',
]


def startProcess(processCmd: list, envVar: dict or None = None):
    for libcPath in libcPaths:
        if os.path.exists(libcPath):  # Locate libc.so file
            break
    return subprocess.Popen(  # start sub-process
        processCmd, env = envVar,
        stdout = subprocess.PIPE, stderr = subprocess.DEVNULL,
        preexec_fn = lambda: ctypes.CDLL(libcPath).prctl(1, signal.SIGTERM)
    )


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


def dnsResolve(domain: str, v6First: bool = False) -> list:
    if v6First:
        return v6Resolve(domain) + v4Resolve(domain)
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


def address2IP(server: str, v6First: bool or None) -> str:
    if isIPv4(server):
        return server  # IPv4 server
    elif isIPv6(server):
        return '[' + ipFormat(server) + ']'  # IPv6 server
    else:
        if v6First is None: v6First = False  # default IPv4 first
        server = dnsResolve(server, v6First = v6First)
        if len(server) == 0:
            raise RuntimeError('invalid domain name resolve')
        return server[0]  # use first IP address
