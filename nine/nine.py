#!/usr/bin/env python3


def digital_root(n):
    """
    keep summing the digits until you get a single-digit number
    
    https://stackoverflow.com/a/39734394/142798
    """
    x = sum(int(digit) for digit in str(n))
    if x < 10:
        return x
    else:
        return digital_root(x)


def main(maxint):
    print('nine')
    for i in range(maxint):
    	v = digital_root(i)
    	if (v == 3):
    		print('**  %d:  %d' % (i, v))
    	elif (v == 6):
    		print('*   %d:   %d' % (i, v))
    	elif (v == 9):
    		print('*** %d: %d' % (i, v))


if __name__ == '__main__':
    main(200)
