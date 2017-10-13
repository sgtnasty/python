#!/usr/bin/env python

# https://pymotw.com/3/os.path/

import os
import os.path
import time
import argparse


APPNAME='lister'
__version__ = '0.0.1'


def config_args():
    """
    Configure command line arguments
    """
    parser = argparse.ArgumentParser(description=APPNAME,
        epilog=("Version {}".format(__version__)))
    #parser.add_argument('-c', metavar='CONFIGFILE', required=False, help='path to config file',
    #    default=DESTINY_CONFIG_FILE)
    #parser.add_argument('--log', metavar='LOGFILE', required=False, help='path to log file',
    #    default=DESTINY_LOGFILE)
    parser.add_argument('files', metavar='F', nargs='+',
                    help='file or directory to evaluate')
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __version__))
    parser.add_argument('--debug', required=False, help='Enable debugging of this script', action="store_true")
    args = parser.parse_args()
    return args


def ftime(filepath):
    print('File         : {}'.format(filepath))
    print('Access time  :', time.ctime(os.path.getatime(filepath)))
    print('Modified time:', time.ctime(os.path.getmtime(filepath)))
    print('Change time  :', time.ctime(os.path.getctime(filepath)))
    print('Size         :', os.path.getsize(filepath))


def finfo(filepath):
    print('File        : {!r}'.format(filepath))
    print('Absolute    :', os.path.isabs(filepath))
    print('Is file?    :', os.path.isfile(filepath))
    print('Is Dir?     :', os.path.isdir(filepath))
    print('Is Link?    :', os.path.islink(filepath))
    print('Mountpoint? :', os.path.ismount(filepath))
    print('Exists?     :', os.path.exists(filepath))
    print('Link Exists?:', os.path.lexists(filepath))


if __name__ == '__main__':
    args = config_args()
    for filepath in args.files:
        #print(type(filepath))
        #print(repr(filepath))
        fp = os.path.abspath(filepath)
        ftime(fp)
        finfo(fp)
