"""
Author: Nolan Rudolph

University of Oregon Netflow Window Isolater

"""

import sys


def main():
    try:
        f = sys.argv[1]
        f_in = open(sys.argv[1], "r")
        start_window = float(sys.argv[2])
        end_window = float(sys.argv[3])
    except IndexError:
        print("Please use as $ python isolateWindow.py [FILE] [START TIME] [END TIME] (both in epoch format)")
        return None

    f_name = f.split(".")
    f_name[1] = "Out." + f_name[1]

    f_out = open(f_name[0] + f_name[1], "w+")

    for entry in f_in:
        entry_list = entry.split(",")

        if start_window <= float(entry_list[0]) <= end_window:
            f_out.write(entry)
        elif float(entry_list[0]) > end_window:
            break

    f_out.close()

    return None


if __name__ == "__main__":
    main()
