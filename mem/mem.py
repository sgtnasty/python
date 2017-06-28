#!/usr/bin/env python3

import sys, os
import subprocess, json


def meminfo():
	mem = {}
	result = subprocess.run(['cat', '/proc/meminfo'], stdout=subprocess.PIPE)
	v = result.stdout.decode('utf-8')
	lines = v.strip().split('\n')
	for line in lines:
		p = line.strip().split(':')
		mem[p[0]] = p[1].strip()		
	print(json.dumps(mem, indent=4, sort_keys=True))


def main():
	meminfo()
	

if __name__ == '__main__':
	main()