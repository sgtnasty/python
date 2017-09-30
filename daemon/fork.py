#!/usr/bin/env python


import os
from subprocess import Popen


def main():
    devnull = open(os.devnull, 'wb')
    Popen(['nohup', 'script.sh'], stdout=devnull, stderr=devnull)


if __name__ == '__main__':
    main()