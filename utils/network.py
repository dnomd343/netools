#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from IPy import IP
from dns import resolver
from utils import logger


def isIPv4(ipAddr: str) -> bool:  # check ipv4 address
    try:
        if '/' in ipAddr:  # exclude cidr input
            return False
        return IP(ipAddr).version() == 4  # ipv4 address
    except:
        return False


def isIPv6(ipAddr: str) -> bool:  # check ipv6 address
    try:
        if '/' in ipAddr:  # exclude cidr input
            return False
        return IP(ipAddr).version() == 6  # ipv6 address
    except:
        return False


def isDomain(domain: str) -> bool:  # check domain format
    try:
        return re.search(  # regex matching
            r'^(?=^.{3,255}$)[a-zA-Z0-9_][a-zA-Z0-9_-]{0,62}(\.[a-zA-Z0-9_][a-zA-Z0-9_-]{0,62})+$', domain
        ) is not None
    except:  # unexpected error
        return False


def isHost(host: str) -> bool:  # confirm ipv4 / ipv6 / domain
    return isIPv4(host) or isIPv6(host) or isDomain(host)


def v4Resolve(domain: str) -> list:  # ipv4 dns resolve
    result = []
    try:
        for ipAddr in resolver.resolve(domain, rdtype = 'A'):
            result.append(ipAddr.to_text())
        return sorted(result, key = lambda x: IP(x).int())
    except:  # resolve error
        return []


def v6Resolve(domain: str) -> list:  # ipv6 dns resolve
    result = []
    try:
        for ipAddr in resolver.resolve(domain, rdtype = 'AAAA'):
            result.append(ipAddr.to_text())
        return sorted(result, key = lambda x: IP(x).int())
    except:  # resolve error
        return []


def dnsResolve(domain: str, v6First: bool = False) -> list:  # dns resolve
    v4Result = v4Resolve(domain)
    v6Result = v6Resolve(domain)
    dnsResult = (v6Result + v4Result) if v6First else (v4Result + v6Result)
    logger.debug('DNS Resolve `%s` -> %s' % (domain, dnsResult))
    return dnsResult


def host2IP(host: str, v6First: bool) -> str:  # convert host to ip address
    if isIPv4(host):
        return str(IP(host))  # ipv4 address
    elif isIPv6(host):
        return '[%s]' % str(IP(host))  # ipv6 server with brackets
    else:
        server = dnsResolve(host, v6First = v6First)  # run dns resolve
        if len(server) == 0:  # no resolve
            raise RuntimeError('Invalid domain name resolve -> %s' % host)
        return server[0]  # use first address
