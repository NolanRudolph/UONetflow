"""
Author: Nolan Rudolph

University of Oregon Netflow Epoch to Grafana Start Date Converter

"""

import sys
from datetime import datetime


def main():
    try:
        f = sys.argv[1]
        f_in = open(f, "r")
    except IndexError:
        print("Please use as $ python " + sys.argv[0] + " [FILE]")
        return None

    f_name = f.split(".")
    f_name[1] = "Out." + f_name[1]

    f_out = open(f_name[0] + f_name[1], "w+")

    for entry in f_in:
        write_line = ""
        entry_list = entry.split(',')[0:15]

        time_start, time_stop = float(entry_list[0]), float(entry_list[1])

        write_time_start = datetime.fromtimestamp(time_start).strftime("%Y-%m-%d %X")
        write_time_stop = datetime.fromtimestamp(time_stop).strftime("%Y-%m-%d %X")

        entry_list[0], entry_list[1] = write_time_start, write_time_stop

        for item in entry_list:
            f_out.write(item + ",")

        f_out.write('\n')

    f_out.close()
    return None


if __name__ == "__main__":
    main()
