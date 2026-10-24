#!/usr/bin/env python3
"""
pyramid1.py

This script prompts the user for a positive integer height and prints a centered
pyramid of asterisks (*) with that many levels.  Each level i (starting at 1)
contains 2*i-1 asterisks, and the line is padded with spaces so that the
pyramid is centered relative to the widest line.

Example output for height 4:
   *
  ***
 *****
*******
"""

def main():
    while True:
        try:
            height = int(input("Enter the height of the pyramid: "))
            if height <= 0:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    for i in range(1, height + 1):
        stars = '*' * (2 * i - 1)
        spaces = ' ' * (height - i)
        print(spaces + stars)

if __name__ == "__main__":
    main()

