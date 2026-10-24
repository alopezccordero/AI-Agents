#!/usr/bin/env python3
"""
This script defines a function `print_pyramid(height)` that prints a centered pyramid of asterisks.
The pyramid has `height` rows. For each row `i` (starting at 1), the number of asterisks is `2*i - 1` and the number of leading spaces is `height - i` to keep the pyramid centered.
The function is then called with a sample height of 5 when the script is executed directly.
"""

def print_pyramid(height):
    """Print a centered pyramid of asterisks with the given height.

    Parameters
    ----------
    height : int
        The number of rows in the pyramid.
    """
    for i in range(1, height + 1):
        spaces = ' ' * (height - i)
        stars = '*' * (2 * i - 1)
        print(spaces + stars)

if __name__ == "__main__":
    # Sample usage: print a pyramid of height 5
    print_pyramid(5)
