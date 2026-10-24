#!/usr/bin/env python3
import sys

def main():
    data = sys.stdin.read().strip().split()
    if len(data) < 2:
        print("Error: need two integers", file=sys.stderr)
        sys.exit(1)
    try:
        a = int(data[0])
        b = int(data[1])
    except ValueError:
        print("Error: inputs must be integers", file=sys.stderr)
        sys.exit(1)
    print(a + b)

if __name__ == "__main__":
    main()
