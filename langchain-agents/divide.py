#!/usr/bin/env python3
import sys

def main():
    try:
        a, b = map(int, sys.stdin.read().strip().split())
    except ValueError:
        print('Error: please provide two integers', file=sys.stderr)
        return
    if b == 0:
        print('Error: Division by zero')
        return
    print(a // b)

if __name__ == '__main__':
    main()
