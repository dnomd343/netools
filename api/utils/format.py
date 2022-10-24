#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def toInt(prefix: str, raw) -> int:  # convert to int
    if isinstance(raw, (int, float)):  # int / float -> int
        return int(raw)
    elif isinstance(raw, bytes):  # bytes -> str
        raw = str(raw, encoding = 'utf-8')
    elif not isinstance(raw, str):
        raise RuntimeError('Field `%s` type not allowed' % prefix)
    try:
        return int(raw)
    except:
        raise RuntimeError('Field `%s` not a integer' % prefix)


def toBool(prefix: str, raw) -> bool:  # convert to bool
    if isinstance(raw, bool):  # bool -> bool
        return raw
    if isinstance(raw, int):  # int -> str
        raw = str(raw)
    elif isinstance(raw, bytes):  # bytes -> str
        raw = str(raw, encoding = 'utf-8')
    elif not isinstance(raw, str):
        raise RuntimeError('Field `%s` type not allowed' % prefix)
    raw = raw.strip().lower()
    if raw == 'true':
        return True
    elif raw == 'false':
        return False
    try:
        raw = int(raw)
        return raw != 0
    except:
        raise RuntimeError('Field `%s` not a boolean' % prefix)
