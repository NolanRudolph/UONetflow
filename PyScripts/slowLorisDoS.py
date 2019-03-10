"""
Author: Nolan Rudolph

Slow Loris DoS Attack Simulator for University of Oregon Netflow Traffic

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
