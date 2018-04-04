#!/usr/bin/env python3

import os
import random
import time
import uuid
import socket
import binascii


def get_remote_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    r = s.getsockname()
    print(repr(r))
    # remote_ip = '{}'.format(r[0])
    s.close()
    return r[0]


def pcount():
    r = random.random()
    time.sleep(r)
    print('{}: {}'.format(r, time.clock()))


def rndip():
    a = 10
    # a = random.randint(10, 254)
    b = random.randint(10, 254)
    c = random.randint(10, 254)
    d = random.randint(10, 254)
    return '{}.{}.{}.{}'.format(a, b, c, d)


def pres(i, source_ip, dest_ip):
    iid = i
    ttl = hex(random.randint(13, 255))
    print("Vr HL TOS  Len   ID   Flg  off TTL Pro  cks      Src      Dst")
    print("4  5  00   5400  {}   0 0000  {}  01 5ac6 {}  {}".format(
        iid, ttl, source_ip, dest_ip))
    r = random.uniform(1.0, 2.5)
    time.sleep(r)
    print('')


def pdumpg(source_ip, dest_ip):
    source_port = random.randint(128, 8192)
    dest_port = random.randint(128, 8192)
    fmt = 'src ip {}: src port {} - dest ip {} : dest port {}'.format(
        source_ip, source_port, dest_ip, dest_port)
    print(fmt)
    time.sleep(random.random())


def trace_tree(source_ip, dest_ip):
    x = binascii.hexlify(os.urandom(32))
    print(x)
    sv = 0
    for i in range(random.randint(8, 32)):
        cluster = ''
        for j in range(64):
            r = random.choices(['.', '*', '+', '~'], weights=[65, 15, 15, 5])
            cluster += r[0]
        hexstr = hex(sv)
        print('{}: {}'.format(hexstr.rjust(8), cluster))
        sv += 32
        time.sleep(random.random() / 2.0)


def main():
    try:
        i = random.randint(1024, 233433)
        source_ip = get_remote_ip()
        while True:
            dest_ip = rndip()
            print('decoding sequence')
            trace_tree(source_ip, dest_ip)
            c = range(random.randint(2, 9))
            print('sending packet {}'.format(uuid.uuid4()))
            for i in c:
                pcount()
            pres(i + 1, source_ip, dest_ip)
            if (random.choice([1, 2, 5]) is 1):
                c = range(random.randint(1, 19))
                for i in c:
                    pdumpg(source_ip, dest_ip)
    except KeyboardInterrupt:
        print('done')


if __name__ == '__main__':
    main()
