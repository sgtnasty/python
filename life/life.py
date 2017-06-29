#!/usr/bin/env python3


import os
import sys
import random


def main():
    print('life begins')
    r = random.SystemRandom()
    for i in range(r.randrange(1, 256)):
        v = r.randint(1, 256)
        print('%d: %d' % (i, v))


if __name__ == "__main__":
    try:
        print('%s running on %s' % (sys.argv[0], os.name))
        main()
    except OSError as err:
        print("OSError: %s" % err)
    except IndexError as err:
        print("IndexError: %s" % err)
    except:
        print("Unexpected error: %s" % sys.exc_info()[0])
