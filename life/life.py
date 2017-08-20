#!/usr/bin/env python3


import os
import sys
import random

adenine = 'A'
cytosine = 'C'
guanine = 'G'
thymine = 'T'
nucleicAcid = ['A', 'G', 'C', 'T']


def getNucleicAcid(r):
    return str(nucleicAcid[r.randint(0, 3)])


def main():
    print('life begins')
    r = random.SystemRandom()
    for i in range(r.randrange(1, 256)):
        nucleicAcid = getNucleicAcid(r)
        print(nucleicAcid, end='')
    print('')


if __name__ == "__main__":
    try:
        print('%s running on %s' % (sys.argv[0], os.name))
        main()
    except OSError as err:
        print("OSError: %s" % err)
    except IndexError as err:
        print("IndexError: %s" % err)
    except:
        ei = sys.exc_info()
        print("Unexpected error: %s" % ei[0])
        print(repr(ei))
