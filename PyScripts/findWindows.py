"""
Author: Nolan Rudolph

University of Oregon Netflow Window Aggregation Finder

"""

import sys


def main():
    f = open(sys.argv[1], "r")

    last_time = 0
    total_entries = 0

    for entry in f:
        entry = entry.split(',')
        cur_time = entry[0]

        if float(cur_time) - float(last_time) > 100:
            print("Last time was " + str(last_time) + " --  Current time is " + str(cur_time))

        last_time = cur_time
        total_entries += 1

    print("Total Entries: " + str(total_entries))
    return None


if __name__ == "__main__":
    main()
