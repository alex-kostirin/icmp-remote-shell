# ICMP remote shell
Prototype of steganography remote shell using ICMP protocol for data
hiding.

To install packet use pip:

`pip install icmp_remote_shell`

Packet provides some common functions can be used in your ICMP
steganography projects:

- checksum - calculates packet checksum
- send_one_ping - sends one ICMP packet
- send_one - as previous but more convenient
- start_sniffing - starts ICMP packets sniffer

Packet also provides to commandline utils for creating remote shell.

**icmp-remote-shell-client** - ICMP remote shell client

Usage:

`icmp-remote-shell-client host_out host_in \[ping_delay\] \[log_file\]`

where:

- host_out - The interface to send requests
- host_in - The interface to listen replies
- ping_delay - Delay between answer pings in seconds, default is 1
- log_file - File to log server answers, default is /var/log/icmp_covert.log


**icmp-remote-shell-server** - ICMP remote shell server

Usage:

`icmp-remote-shell-server host \[ping_delay\]`

where:

- host - The interface to listen request
- ping_delay - Delay between answer pings in seconds, default is 1

>Note: commands should run under user with privileges to send ICMP
>messages only

**Contribution**

Fell free ro contribute to this project using
[github](https://github.com/alex-kostirin/icmp-remote-shell) or
[gitlab](https://gitlab.com/alex-kostirin/icmp-remote-shell).




