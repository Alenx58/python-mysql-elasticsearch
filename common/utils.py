#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author : Alenx.Hai <alenx.hai@gmail.com>
# created time: 2020/12/17-7:32 下午
import time
from functools import wraps


def timer(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        print(f"{method.__name__} => {(end_time-start_time)*1000} ms")

        return result

    return wrapper
