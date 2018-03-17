#!/usr/bin/env python3

import os
import random
import time
import logging
import uuid



def config_log():
    log = logging.getLogger('cmonitor')
    f = logging.Formatter('%(asctime)s - %(name)s:%(process)d - %(levelname)s - %(message)s')
    h = logging.StreamHandler()
    h.setLevel(logging.DEBUG)
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.DEBUG)
    return log

def mon_cpu():
    return random.choice([
        '0x283FE8',
        '#AFEFEF',
        '2398098098'
        ])

def mon_slice():
    s = random.random()
    return random.choice([
        'Created slice User Slice of root.',
        'Starting User Slice of root.',
        'Started Session {} of user root.'.format(s),
        'Starting Session {} of user root.'.format(s),
        'Removed slice User Slice of root.' 
        ])

def monitor(log):
    while True:
        time.sleep(random.random())
        xsel = [1,   2,   3,   4,   5]
        xwei = [0.3, 0.1, 0.1, 0.3, 0.2]
        x = random.choices(xsel, xwei)[0]
        #log.debug('weight={}'.format(x))
        if x == 1:
            log.info('process {}'.format(uuid.uuid4()))
        elif x == 2:
            log.warn('interrupt 0x93')
        elif x == 3:
            log.error('internal register corruption: 0x4343d3')
        elif x == 4:
            log.debug(mon_slice())
        else:
            log.info('continue processing on to next slice')
        time.sleep(random.random() / 2)

if __name__ == "__main__":
    log = config_log()
    sessionid = uuid.uuid4()
    log.info('cmonitor starting {}'.format(sessionid))
    try:
        monitor(log)
    except KeyboardInterrupt as e:
        log.info('KeyboardInterrupt {}'.format(e))
        