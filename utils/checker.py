#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# TODO: checker -> option check

# type / value(lambda)

def checker(limit: dict, *args) -> None:
    if len(limit) != len(args):
        raise RuntimeError('Args number error')

    # for i in range()

    print(args[0])
    print(len(args))
