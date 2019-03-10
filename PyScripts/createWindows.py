"""
Author: Nolan Rudolph

University of Oregon Netflow Aggregation Tool

"""

import sys


def main():

    try:
        f = open(sys.argv[1], "r")
        split_time = float(sys.argv[2])
        briefing = int(sys.argv[3])
        offset = int(sys.argv[4])
        location = sys.argv[5]
    except IndexError:
        print("Please use $ python createWindows.py [FILE] [AGGREGATION TIME IN SECONDS] [BRIEFING] [OFFSET] [DESTINATION]")
        print("FILE: The file you want to read from.")
        print("AGGREGATION TIME IN SECONDS: What time interval would you like to aggregate by?")
        print("BRIEFING: Provides a space the length of [AGGREGATION TIME IN SECONDS] between time intervals.")
        print("OFFSET: If BRIEFING == 1, you can specify offset, essentially even or odd intervals.")
        print("DESTINATION: Where would you like to output the aggregated sets to?")
        return None

    create_windows(f, split_time, briefing, offset, location)

    return None


def create_windows(f, split_time, briefing, offset, location):
    # Initialize mutable values
    split_count = 0

    # Read first line to gather basis of first split
    first = f.readline().split(",")
    base_time = float(first[0])

    # Create starting file to write to
    newF = open("./" + location + "/segData" + str(split_count) + ".csv", "w+")

    if briefing:
        freeze = 0  # Freeze is used to not record gaps between aggregations

        # Setup first file to write to
        newF = open("./" + location + "/segData" + str(split_count) + ".csv", "w+")

        # Initialize first window
        if offset:
            begin_window = split_time
            end_window = split_time * 2
        else:
            begin_window = 0
            end_window = split_time

        for entry in f:
            seg = float(entry.split(",")[0])

            if begin_window <= (seg - base_time) <= end_window:
                newF.write(entry)
                freeze = 1
            elif freeze == 1:
                print(str(begin_window) + " < " + str(seg) + " !< " + str(end_window))
                begin_window += split_time * 2
                end_window += split_time * 2
                split_count += 1
                newF = open("./" + location + "/segData" + str(split_count) + ".csv", "w+")
                freeze = 0
    else:
        for entry in f:
            seg = float(entry.split(",")[0])

            if seg - base_time < split_time:
                newF.write(entry)
            else:
                print(str(seg) + " is more than " + str(split_time) + " second(s) larger than " + str(base_time) + " -- " + str(seg-base_time))
                base_time = seg
                split_count += 1
                newF = open("./" + location + "/segData" + str(split_count) + ".csv", "w+")
                newF.write(entry)


    return None


if __name__ == "__main__":
    main()
