"""
Author: Nolan Rudolph

Slow Loris DoS Attack Simulator for University of Oregon Netflow Traffic

"""
import sys
from random import randrange, choice

UDP_ports = range(0, 65535)
TCP_ports = range(0, 65535)

used_UDP_ports = []
used_TCP_ports = []

to_connect = []
cur_connect = []

def main():
    try:
        f_in = sys.argv[1]
        brief_period = int(sys.argv[2])
        start_window = float(sys.argv[3])
        end_window = float(sys.argv[4])
    except IndexError:
        print("Please use as $ python " + sys.argv[0] + " [FILE] [BRIEF] [START TIME] [END TIME] (both in epoch format)")
        return None

    forge_connections(f_in)

    f_out = open("spoofedLorisAttack.csv", "w+")

    implement_connections(f_in, f_out, brief_period, start_window, end_window)

    f_out.close()

    return None


def forge_connections(f):
    TCP_len = 65534
    total_len = 65535*2-2
    grab_IPs = 0

    f = open(f, "r")

    for entry in f:
        entry_list = entry.split(',')

        if grab_IPs < total_len:
            gen_srcIP = entry_list[2]
            gen_dstIP = entry_list[3]
            gen_dstPort = entry_list[5]
            gen_TOS = entry_list[7]
            gen_TCP_flags = entry_list[8]
            gen_rout_in = entry_list[11]
            gen_rout_out = entry_list[12]
            gen_src_ASN = entry_list[13]
            gen_dst_ASN = entry_list[14]

            if TCP_len > 0:
                gen_srcPort = choice(TCP_ports)
                TCP_ports.remove(gen_srcPort)
                TCP_len = TCP_len - 1
                prot = 6
            else:
                gen_srcPort = choice(UDP_ports)
                UDP_ports.remove(gen_srcPort)
                prot = 17

            gen_bytes = str(randrange(40, 80))

            to_connect.append((gen_srcIP, gen_dstIP, gen_srcPort, gen_dstPort, prot, gen_TOS, gen_TCP_flags, gen_bytes,
                               gen_rout_in, gen_rout_out, gen_src_ASN, gen_dst_ASN))
            grab_IPs += 1

        else:
            return None


def implement_connections(f_in, f_out, brief_period, start_window, end_window):
    # To be adjusted in future projects
    dTime = (end_window - start_window) / (100000)

    f_in = open(f_in, "r")

    first_line = f_in.readline().split(',')

    base_time = float(first_line[0])

    for entry in f_in:
        entry_list = entry.split(',')
        src_port = int(entry_list[4])
        prot = entry_list[6]
        cur_time = float(entry_list[0])

        if prot == 6 and src_port not in used_TCP_ports:
            f_out.write(entry)
        elif prot == 17 and src_port not in used_UDP_ports:
            f_out.write(entry)
        elif prot != 6 and prot != 17:
            f_out.write(entry)

        if cur_time - base_time >= dTime and brief_period <= 0:
            new_con = choice(to_connect)
            to_connect.remove(new_con)

            if int(new_con[4]) == 6:
                used_TCP_ports.append(new_con[2])
            else:
                used_UDP_ports.append(new_con[2])

            f_out.write("{},{},{},{},{},{},{},{},{},1,{},{},{},{},{},\n".format(str(cur_time+0.001), str(cur_time+0.002),
                                                                              str(new_con[0]), str(new_con[1]),
                                                                              str(new_con[2]), str(new_con[3]),
                                                                              str(new_con[4]), str(new_con[5]),
                                                                              str(new_con[6]), str(new_con[7]),
                                                                              str(new_con[8]), str(new_con[9]),
                                                                              str(new_con[10]), str(new_con[11])))
            base_time = cur_time

        brief_period = brief_period - 1

    return None


if __name__ == "__main__":
    main()
