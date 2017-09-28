#!/usr/bin/env python

FILE='weapons.md'

f = open(FILE)
s = f.readlines()
f.close()
r = []
for i in s:
    v = i.strip()
    if not v.startswith('#'):
        if len(v) > 0:
            r.append(i)
t = set(r)
for x in t:
    print(x)