#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
from time import sleep

def segment(s=[]):
    m = "█"
    if len(s) != 7:
        s = [1 for i in range(7)]
    def dm(*c):
        return m if 1 in [s[x] for x in c] else " "
    return dm(0,1)*3+dm(0)*10+dm(0,2)*3+"\n"+\
        (dm(1)*3+" "*10+dm(2)*3+"\n")*5+\
        dm(1,4,3)*3+dm(3)*10+dm(2,5,3)*3+"\n"+\
        (dm(4)*3+" "*10+dm(5)*3+"\n")*5+\
        dm(4,6)*3+dm(6)*10+dm(5,6)*3

def mergestuff(s):
    r=["" for i in range(13)]
    for p in s:
        for i in range(13):
            r[i]+=p.split('\n')[i].strip('\n')+"  "
    return '\n'.join(r)

def main():
    numbers = [
        segment([1,1,1,0,1,1,1]), #0
        segment([0,0,1,0,0,1,0]), #1
        segment([1,0,1,1,1,0,1]), #2
        segment([1,0,1,1,0,1,1]), #3
        segment([0,1,1,1,0,1,0]), #4
        segment([1,1,0,1,0,1,1]), #5
        segment([1,1,0,1,1,1,1]), #6
        segment([1,0,1,0,0,1,0]), #7
        segment([1,1,1,1,1,1,1]), #8
        segment([1,1,1,1,0,1,1])  #9
    ]
    blinker = ["   \n"*3+"███\n"*2+"   \n"*3+"███\n"*2+"   \n"*3, "   \n"*13]

    while True:
        sleep(0.5)
        now = datetime.now()
        hour = str(now.hour) if len(str(now.hour)) == 2 else "0"+str(now.hour)
        minute = str(now.minute) if len(str(now.minute)) == 2 else "0"+str(now.minute)
        fb = [numbers[int(i)] for i in hour+minute]
        fb.insert(2,blinker[now.second%2])
        frame = mergestuff(fb)
        print "\033c"+frame+'\r'


if __name__ == "__main__":
    main()