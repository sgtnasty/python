#!/usr/bin/env python

import os
import uuid


def generate_uuid():
    s = uuid.uuid1()
    print(s)
    print(repr(s.fields))


def generate_temp_password(length):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijklmnopqrstuvwxyz"
    return "".join(chars[ord(c) % len(chars)] for c in os.urandom(length))


def generate_urandom(length):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")
    d = os.urandom(length)
    v = map(ord, os.urandom(length))
    return v


if __name__ == '__main__':
    v = generate_urandom(32)
    print(v)
    v = generate_temp_password(16)
    print(v)
    v = generate_temp_password(32)
    print(v)
