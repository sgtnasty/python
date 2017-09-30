#!/usr/bin/env python


import random
import json


class Testor(object):
    """docstring for Testor"""
    def __init__(self, *args, **kwargs):
        super(Testor, self).__init__()
        print('Testor: ', args, kwargs)
        obj = json.dumps(kwargs)
        print(obj)


if __name__ == '__main__':
    print('run 1')
    p = Testor('Cayde-6', species='Exo', level=40, pclass='Hunter')
    print(repr(p))