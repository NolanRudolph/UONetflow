"""
Author: Nolan Rudolph

University of Oregon Netflow Anomaly Finder

"""

import sys, socket, whois
from whois import whois
from pprint import pprint
packets = []

def main():
    try:
        f_in = open(sys.argv[1], "r")
    except IndexError:
        print("Please run as $ python findAnomalies.py [FILE]")
        return None

    f_out = open("summary.txt", "w+")

    for entry in f_in:
        entry_list = entry.split(',')

        start_time_norm = entry_list[0]
        start_time_prefix = start_time_norm[0:2]
        end_time_norm = entry_list[1]
        threshold = int(entry_list[2]) * 1000000
        start_time_epoch = entry_list[3]
        end_time_epoch = entry_list[4]

        if start_time_prefix == '08':
            find_entry("MORNING", start_time_norm, end_time_norm, start_time_epoch, end_time_epoch, threshold, f_out)
        elif start_time_prefix == '12':
            find_entry("AFTERNOON", start_time_norm, end_time_norm, start_time_epoch, end_time_epoch, threshold, f_out)
        elif start_time_prefix == '18':
            find_entry("EVENING", start_time_norm, end_time_norm, start_time_epoch, end_time_epoch, threshold, f_out)
        elif start_time_prefix == '22':
            find_entry("NIGHT", start_time_norm, end_time_norm, start_time_epoch, end_time_epoch, threshold, f_out)

    f_out.close()

    return None


def find_entry(dataset, start_time_norm, end_time_norm, start_time_epoch, end_time_epoch, threshold, f_out):
    f = open(dataset, "r")

    for entry in f:


        entry_list = entry.split(',')
        comp_time = entry_list[0]
        byte_count = int(entry_list[10])

        if start_time_epoch <= comp_time <= end_time_epoch and byte_count >= threshold:
            f_out.write("~ FROM {} TO {} ~".format(start_time_norm, end_time_norm))
            src_IP = entry_list[2]
            dst_IP2 = entry_list[3]

            f_out.write("\nFound entry with " + str(byte_count) + " bytes.\n")
            f_out.write("Entry: " + entry + "\n")
            try:
                f_out.write("Source:\n" + str(whois(src_IP)) + "\n")
                f_out.write("Destination:\n" + str(whois(dst_IP2)) + "\n")
            except:
                f_out.write("Analyze " + entry + "\n")

            f_out.write("\n--------------------------------------------------------\n")

    return None


if __name__ == "__main__":
    main()
