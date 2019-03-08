import sys


def main():

    try:
        f = open(sys.argv[1], "r")
        split_time = float(sys.argv[2])
        offset = int(sys.argv[3])
        location = sys.argv[4]
    except IndexError:
        print("Please use as $ python createWindows.py [FILE] [AGGREGATION TIME IN SECONDS] [OFFSET] [DESTINATION]")

    # Read first line to gather basis of first split
    first = f.readline().split(",")
    base_time = float(first[0])

    # Initialize mutable values
    split_count = 0
    freeze = 0  # Freeze is used to not record gaps between aggregations

    # Setup first file to write to
    newF = open("./" + location + "/segData" + str(split_count), "w+")

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
            begin_window += split_time * 2
            end_window += split_time * 2
            split_count += 1
            newF = open("./" + location + "/segData" + str(split_count), "w+")
            freeze = 0


    return None


if __name__ == "__main__":
    main()
