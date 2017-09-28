#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser(prog='mydaemon')
parser.add_argument('--g')
sp = parser.add_subparsers()
sp_start = sp.add_parser('start', help='Starts %(prog)s daemon')
sp_stop = sp.add_parser('stop', help='Stops %(prog)s daemon')
sp_restart = sp.add_parser('restart', help='Restarts %(prog)s daemon')

args = parser.parse_args()

print('***')
print(repr(args))