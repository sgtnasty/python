#!/usr/bin/env python

from ds_store import DSStore

import json

path = '~/.DS_Store'


def parse(file):
    filelist = []
    for i in file:
        if i.filename != '.':
            filelist.append(i.filename)
            return list(set(filelist))


d = DSStore.open(path, 'r+')
fileresult = parse(d)
print(json.dumps(fileresult))
for name in fileresult:
    try:
        d = DSStore.open(path + name + '/.DS_Store', 'r+')
        fileresult = parse(d)
        all.append(fileresult)
        print(json.dumps(fileresult))
    except:
        pass
