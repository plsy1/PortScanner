#!/usr/bin/env python3
import argparse
import sys
from iface import *
from cli import *


def main():
    parser = argparse.ArgumentParser(
        description="LAN host and port scanner. Supports interactive, full-auto, and single-IP port range modes."
    )
    parser.add_argument(
        "-n",
        "--network",
        type=str,
        help="Target network in CIDR format, e.g., 192.168.0.0/24",
    )
    parser.add_argument(
        "-p",
        "--ports",
        type=str,
        help="Comma-separated list of ports to scan, e.g., 22,80,443",
    )
    parser.add_argument(
        "-i", "--iface", type=str, help="Network interface to use, e.g., eth0"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Full automatic mode: scan all hosts and selected ports without interaction",
    )
    parser.add_argument("--ip", type=str, help="Single IP address to scan")
    parser.add_argument(
        "--portrange", type=str, help="Port range to scan for single IP, e.g., 20-1024"
    )
    parser.add_argument(
        "--threads", type=int, default=50, help="Max concurrent threads"
    )

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    iface = args.iface or get_default_iface_name()

    # Single IP + port range mode
    if args.ip and args.portrange:
        scan_single_ip(args.ip, args.portrange, threads=args.threads)
        return

    # Interactive or full-auto network scan
    network = args.network or input("Enter target network (e.g., 192.168.0.0/24): ")
    ports = args.ports or input(
        "Enter ports to scan (comma separated, e.g., 22,80,443): "
    )

    if args.all:
        full_auto_scan(network, iface, ports)
    else:
        interactive_scan(network, iface, ports)


if __name__ == "__main__":
    main()
