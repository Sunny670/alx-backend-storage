#!/usr/bin/env python3
"""Redis and Python exercise"""
import uuid
from functools import wraps
from typing import Callable, Union

import redis


def count_calls(method: Callable) -> Callable:
    """decorator that takes a single method Callable argument
    and returns a Callable"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """increments the count for that key every time the method
        is called and returns the value returned by the original method """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """stores the history of inputs and outputs for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """saves the input and output of each function in redis
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        output = method(self, *args, **kwargs)

        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper

