#!/usr/bin/env python

import os
import uuid


if __name__ == '__main__':
    d = os.urandom(32)
    s = uuid.uuid1()
    print(s)
    print(repr(s.fields))
