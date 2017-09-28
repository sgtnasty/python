#!/usr/bin/env python
 
import sys, time
from daemon import Daemon
import argparse
import errno
import logging
from my_service import MyDaemon



__version__ = 'MY Queue Manager 2.01'


# Global vars
MY_DIR='/etc/my'
MY_LOGFILE = '/var/log/my.log'
MY_CONFIG_FILE = '/etc/my/my.json'
#MY_DB_FILE = '/var/my/my.db'
#MY_QUEUE_DIR = '/var/my/queue'


def config_args():
    """
    Configure command line arguments
    """
    parser = argparse.ArgumentParser(description='MY Queue Manager',
        epilog=("Version {}".format(__version__)))
    ### -------------- DAEMON COMMANDS - mutually exlusive
    ###
    ###
    ###
    ###
    ### ----------------------------------------------------------------------------------------
    parser.add_argument('-c', metavar='CONFIGFILE', required=False, help='path to config file',
        default=MY_CONFIG_FILE)
    parser.add_argument('--log', metavar='LOGFILE', required=False, help='path to log file',
        default=MY_LOGFILE)
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __version__))
    parser.add_argument('--debug', required=False, help='Enable debugging of this script', action="store_true")
    args = parser.parse_args()
    return args


def config_log(args):
    """
    Configure Python Logging Module
    """
    # create logger
    logger = logging.getLogger('my-queuemanager')
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s:%(process)d - %(levelname)s - %(message)s')
    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    # create file handler
    try:
        fh = logging.FileHandler(args.log)
        fh.setLevel(logging.DEBUG)
        # add formatter to fh
        fh.setFormatter(formatter)
        # add fh to logger
        logger.addHandler(fh)
        logger.setLevel(logging.INFO)
    except IOError as e:
        logger.error("Unable to open log file:%s, reason = %s" % (MY_LOGFILE, errno.errorcode[e[0]]))
    if (args.debug):
        # make sure to set both Handlers to the DEBUG level
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
        logger.debug("DEBUG Enabeled")
        logger.debug("args=%s" % repr(args))
    return logger


def config_my(args, log):
    """
    Read the MY config file from JSON
    """
    try:
        fh = open(args.c)
        my = json.load(fh)
        fh.close()
    except:
        log.error('Error reading config file. %s: %s' % (sys.exc_type, sys.exc_value))
        sys.exit(1)
    if (args.debug):
        log.debug("my=%s" % repr(my))
    return my

 
if __name__ == "__main__":
    args = config_args()
    log = config_log(args)
    my = config_my(args, log)
    daemon = MyDaemon('/tmp/myd.pid', args, log, my)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)