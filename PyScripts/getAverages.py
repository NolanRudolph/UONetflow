"""
Author: Nolan Rudolph

University of Oregon Netflow Traffic Averager

"""

import sys

def main():
    try:
        f_in = open(sys.argv[1], "r")
    except IndexError:
        print("Please run as $ python " + sys.argv[0] + " [FILE]")
        return None

    src_ports = {}
    dst_ports = {}
    prots = {}
    TOSs = {}
    TCP_flags = {}
    packet_totals = 0
    byte_totals = 0
    rout_ins = {}
    rout_outs = {}
    src_ASNs = {}
    dst_ASNs = {}

    for entry in f_in:
        entry_list = entry.split(',')

        src_port = entry_list[4]
        dst_port = entry_list[5]
        prot = entry_list[6]
        TOS = entry_list[7]
        TCP_flag = entry_list[8]
        packets = float(entry_list[9])
        bytes = float(entry_list[10])
        rout_in = entry_list[11]
        rout_out = entry_list[12]
        src_ASN = entry_list[13]
        dst_ASN = entry_list[14]

        # Source Port
        if src_port in src_ports:
            src_ports[src_port] = src_ports[src_port] + 1
        else:
            src_ports[src_port] = 1

        # Destination Port
        if dst_port in dst_ports:
            dst_ports[dst_port] = dst_ports[dst_port] + 1
        else:
            dst_ports[dst_port] = 1

        # Protocol
        if prot in prots:
            prots[prot] = prots[prot] + 1
        else:
            prots[prot] = 1

        # Type of Service
        if TOS in TOSs:
            TOSs[TOS] = TOSs[TOS] + 1
        else:
            TOSs[TOS] = 1

        # TCP Flags
        if TCP_flag in TCP_flags:
            TCP_flags[TCP_flag] = TCP_flags[TCP_flag] + 1
        else:
            TCP_flags[TCP_flag] = 1

        # Number of Packets
        packet_totals = packet_totals + packets

        # Number of Bytes
        byte_totals = byte_totals + bytes

        # Router Ingress Port
        if rout_in in rout_ins:
            rout_ins[rout_in] = rout_ins[rout_in] + 1
        else:
            rout_ins[rout_in] = 1

        # Router Egress Port
        if rout_out in rout_outs:
            rout_outs[rout_out] = rout_outs[rout_out] + 1
        else:
            rout_outs[rout_out] = 1

        # Source Autonomous Network
        if src_ASN in src_ASNs:
            src_ASNs[src_ASN] = src_ASNs[src_ASN] + 1
        else:
            src_ASNs[src_ASN] = 1

        # Destination Autonomous Network
        if dst_ASN in dst_ASNs:
            dst_ASNs[dst_ASN] = dst_ASNs[dst_ASN] + 1
        else:
            dst_ASNs[dst_ASN] = 1

    bytes_per_packet = byte_totals/packet_totals

    most_src_port = max(src_ports, key=src_ports.get)
    most_dst_port = max(dst_ports, key=dst_ports.get)
    most_prot = max(prots, key=prots.get)
    most_TOS = max(TOSs, key=TOSs.get)
    most_TCP_flag = max(TCP_flags, key=TCP_flags.get)
    most_rout_in = max(rout_ins, key=rout_ins.get)
    most_rout_out = max(rout_outs, key=rout_outs.get)
    most_src_ASN = max(src_ASNs, key=src_ASNs.get)
    most_dst_ASN = max(dst_ASNs, key=dst_ASNs.get)

    print("+---------------------- PACKETS + BYTES ----------------------+")
    print("|                                                             |")
    print("|      Total Packets received/delivered was {}                |".format(packet_totals))
    print("|       Total Bytes received/delivered was {}                 |".format(byte_totals))
    print("|            Average Bytes/Packet was {}                      |".format(bytes_per_packet))
    print("|                                                             |")
    print("+--------------------------- PORTS ---------------------------+")
    print("|                                                             |")
    print("|           Most common Source Port was {} at {}              |".format(most_src_port, src_ports[most_src_port]))
    print("|         Most common Destination Port was {} at {}           |".format(most_dst_port, dst_ports[most_dst_port]))
    print("|       Most common Router Ingress Port was {} at {}          |".format(most_rout_in, rout_ins[most_rout_in]))
    print("|       Most common Router Egress Port was {} at {}           |".format(most_rout_out, rout_outs[most_rout_out]))
    print("|                                                             |")
    print("+------------------------- PROTOCOL --------------------------+")
    print("|                                                             |")
    print("|       Most common IP Protocol was {} at {}                  |".format(most_prot, prots[most_prot]))
    print("|                                                             |")
    print("+------------------------ TOS + TCP --------------------------+")
    print("|           Most common TOS was {} at {}                      |".format(most_TOS, TOSs[most_TOS]))
    print("|       Most common TCP Flags were {} at {}                   |".format(most_TCP_flag, TCP_flags[most_TCP_flag]))
    print("|                                                             |")
    print("+------------------- AUTONOMOUS NETWORKS ---------------------+")
    print("|                                                             |")
    print("|     Most common Source Autonomous Network was {} at {}      |".format(most_src_ASN, src_ASNs[most_src_ASN]))
    print("|   Most common Destination Autonomous Network was {} at {}   |".format(most_dst_ASN, dst_ASNs[most_dst_ASN]))
    print("|                                                             |")
    print("+-------------------------------------------------------------+")


if __name__ == "__main__":
    main()
