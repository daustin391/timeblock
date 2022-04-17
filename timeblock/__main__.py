""" Timeblock
    A script for breaking up a day into scheduled blocks of time

"""

from timeblock.sql import TimeblockDB


def main():
    """Prompt for input and print schedule"""
    with TimeblockDB() as db:
        while True:
            item = input()
            if item.casefold() == "x":
                break


if __name__ == "__main__":
    main()
