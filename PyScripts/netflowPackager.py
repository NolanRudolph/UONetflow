import sys, random
from scapy.all import *
from scapy.contrib.igmp import *
from scapy.contrib.bgp import *

packets = []

def main():
    try:
        f_in = open(sys.argv[1], "r")
        f_out = sys.argv[2]
    except IndexError:
        print("Please run as $ python netflowPackager.py [FILE] [DIRECTORY TO WRITE TO]")
        return None

    for entry in f_in:
        entry = entry.split(',')

        # Create informative variables to segregate data into
        start_time = float(entry[0])
        end_time = float(entry[1])
        src_IP = str(entry[2])
        dst_IP = str(entry[3])
        src_port = int(float(entry[4]))
        dst_port = int(float(entry[5]))
        IP_prot = int(entry[6])
        TOS_val = int(entry[7])
        TCP_flags = int(entry[8])
        num_packets = int(entry[9])
        bytes = int(entry[10])
        router_in = int(entry[11])
        router_out = int(entry[12])
        src_ASN = int(entry[13])
        dst_ASN = int(entry[14])

        # Begin creation of synthesized packet
        p = IP()
        dTime = get_time(start_time, end_time)

        # Create a IPv4 or IPv6 packet based on contents
        is_ipv6 = False
        for char in src_IP:
            if char == ":":
                p = gen_IPv6(src_IP, dst_IP, src_port, dst_port, IP_prot, TCP_flags, num_packets, bytes, dTime)
                is_ipv6 = True

        if not is_ipv6:
            p = gen_IPv4(src_IP, dst_IP, src_port, dst_port, IP_prot, TOS_val, TCP_flags, num_packets, bytes, dTime)

        # Add other attributes to be utilized in visualizations that couldn't be utilized by Scapy
        p.router_in = router_in
        p.router_out = router_out
        p.src_ASN = src_ASN
        p.dst_ASN = dst_ASN

        for _ in range(num_packets):
            packets.append(p)

    wrpcap(f_out, packets)
    return None


# Accepts epoch format
def get_time(start, end):
    return end - start

def calc_IPv4_overhead(IP_prot, src_IP, dst_IP, src_port, dst_port, TOS_val, TCP_flags, packets, dTime):
    # Init packet
    p = IP()

    # ICMP Protocol
    if IP_prot == 1:
        # * This will only work with University of Oregon ICMP Netflow *
        # Discard for other netflows, or derive type and code another way
        type, code = dst_port.split('.')

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            ICMP(type=type, code=code)

    # IGMP Protocol
    if IP_prot == 2:
        # * This will only work with University of Oregon ICMP Netflow *
        # Discard for other netflows, or derive type and code another way
        type, code = dst_port.split('.')

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            IGMP(type=type, mrcode=code)

    # TCP Protocol
    elif IP_prot == 6:

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            TCP(sport=src_port, dport=dst_port, flags=TCP_flags, window=dTime)

    # UDP Protocol
    elif IP_prot == 17:

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            UDP(sport=src_port, dport=dst_port)

    # GRE (Generic Routing Encapsulation) Protocol
    elif IP_prot == 47:

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            GRE()

    # ESP (Encapsulating Security Payload) Protocol
    elif IP_prot == 50:

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            ESP()

    # Rare packets
    else:
        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val)

    return p


# "Until IPv6 is in general use, the flow label is mostly experimental. Uses and controls involving flow labels have
#  not yet been defined nor standardized." Therefore, I will not choose to include flow labels as an IPv6 argument.
def calc_IPv6_overhead(IP_prot, src_IP, dst_IP, src_port, dst_port, TCP_flags, dTime):
    # Init packet
    p = IPv6()

    # ICMP Protocol
    if IP_prot == 1:
        # * This will only work with University of Oregon ICMP Netflow *
        # Discard for other netflows, or derive type and code another way
        type, code = dst_port.split('.')

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            ICMP(type=type, code=code)

    # IGMP Protocol
    if IP_prot == 2:
        # * This will only work with University of Oregon ICMP Netflow *
        # Discard for other netflows, or derive type and code another way
        type, code = dst_port.split('.')

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            IGMP(type=type, mrcode=code)

    # TCP Protocol
    elif IP_prot == 6:

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            TCP(sport=src_port, dport=dst_port, flags=TCP_flags, window=dTime)

    # UDP Protocol
    elif IP_prot == 17:

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            UDP(sport=src_port, dport=dst_port, window=dTime)

    # GRE (Generic Routing Encapsulation) Protocol
    elif IP_prot == 47:

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            GRE()

    # ESP (Encapsulating Security Payload) Protocol
    elif IP_prot == 50:

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            ESP()

    # ICMP Protocol for IPv6
    elif IP_prot == 58:
        # * This will only work with University of Oregon ICMP Netflow *
        # Discard for other netflows, or derive type and code another way
        type, code = dst_port.split('.')

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            ICMP(type=type, code=code)

    # OSPF Protocol (Assuming OSPF Hello Packet)
    elif IP_prot == 89:
        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            OSPF_Hello(hellointerval=dTime)

    # Rare packets
    else:
        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot)

    return p


def gen_IPv4(src_IP, dst_IP, src_port, dst_port, IP_prot, TOS_val, TCP_flags, packets, bytes, dTime):
    # Init packet
    p = IP()

    overhead = calc_IPv4_overhead(IP_prot, src_IP, dst_IP, src_port, dst_port, TOS_val, TCP_flags, packets, dTime)

    # This creates a tiny degree of error
    bytes_left = bytes - len(overhead) * packets
    packet_size = int(bytes_left/packets)

    # Create a fake payload that justifies byte count of packets to correct amount
    payload = bytearray(random.getrandbits(8) for _ in xrange(packet_size))

    if IP_prot == 1:
        type, code = dst_port.split('.')

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            ICMP(type=type, code=code, length=packet_size) / Raw(payload)

    elif IP_prot == 2:
        type, code = dst_port.split('.')

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            IGMP(type=type, mrcode=code) / Raw(payload)

    elif IP_prot == 6:

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            TCP(sport=src_port, dport=dst_port, flags=TCP_flags) / Raw(payload)

    elif IP_prot == 17:

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            UDP(sport=src_port, dport=dst_port, len=packet_size) / Raw(payload)

    elif IP_prot == 47:

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            GRE() / Raw(payload)

    elif IP_prot == 50:

        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            ESP(data=payload)

    else:
        p = IP(src=src_IP, dst=dst_IP, proto=IP_prot, tos=TOS_val, chksum=packets) / \
            Raw(payload)

    return p


def gen_IPv6(src_IP, dst_IP, src_port, dst_port, IP_prot, TCP_flags, packets, bytes, dTime):
    # Init packet
    p = IPv6()

    overhead = calc_IPv6_overhead(IP_prot, src_IP, dst_IP, src_port, dst_port, TCP_flags, packets)

    # This creates a tiny degree of error
    bytes_left = bytes - len(overhead) * packets
    packet_size = int(bytes_left/packets)

    # Create a fake payload that justifies byte count of packets to correct amount
    payload = bytearray(random.getrandbits(8) for _ in xrange(packet_size))

    if IP_prot == 1:
        type, code = dst_port.split('.')

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            ICMP(type=type, code=code, length=packet_size) / Raw(payload)

    elif IP_prot == 2:
        type, code = dst_port.split('.')

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            IGMP(type=type, mrcode=code) / Raw(payload)

    elif IP_prot == 6:
        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            TCP(sport=src_port, dport=dst_port, flags=TCP_flags) / Raw(payload)

    elif IP_prot == 17:

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            UDP(sport=src_port, dport=dst_port, len=packet_size) / Raw(payload)

    elif IP_prot == 47:

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            GRE() / Raw(payload)

    elif IP_prot == 50:

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            ESP(data=payload)

    elif IP_prot == 58:
        type, code = dst_port.split('.')

        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            ICMP(type=type, code=code) / \
            Raw(payload)

    elif IP_prot == 89:
        p = IPv6(src=src_IP, dst=dst_IP, nh=IP_prot) / \
            OSPF_Hello(hellointerval=dTime) / \
            Raw(payload)

    return p

if __name__ == "__main__":
    main()
