from iface import *

import socket
import struct
import time


def generate_arp_request_packet(target_ip, iface="eth0"):
    """
    Build an ARP request packet to query the MAC address of a target IP.

    Args:
        target_ip (str): The target IP address.
        iface (str): Local network interface name, default is "eth0".

    Returns:
        bytes: The complete Ethernet frame containing the ARP request.
    """
    src_ip, src_mac = get_iface_info_by_name(iface)
    src_mac_bytes = bytes.fromhex(src_mac.replace(":", ""))
    src_ip_bytes = socket.inet_aton(src_ip)
    target_ip_bytes = socket.inet_aton(target_ip)
    broadcast_mac = b"\xff\xff\xff\xff\xff\xff"

    # Ethernet header: dst_mac + src_mac + ethertype(0x0806 ARP)
    eth_hdr = broadcast_mac + src_mac_bytes + struct.pack("!H", 0x0806)

    # ARP header: htype, ptype, hlen, plen, opcode(1=request), src_mac, src_ip, dst_mac, dst_ip
    arp_hdr = struct.pack(
        "!HHBBH6s4s6s4s",
        1,  # htype Ethernet
        0x0800,  # ptype IPv4
        6,  # hlen
        4,  # plen
        1,  # opcode 1=ARP request
        src_mac_bytes,
        src_ip_bytes,
        b"\x00" * 6,  # target MAC unknown
        target_ip_bytes,
    )

    return eth_hdr + arp_hdr


def arp_ping(target_ip, iface="eth0", timeout=1):
    """
    Check if a host is online by sending an ARP request.

    Args:
        target_ip (str): The target IP address.
        iface (str): Local network interface name.
        timeout (float): Timeout in seconds to wait for a reply.

    Returns:
        bool: True if the host responds, False otherwise.
    """
    raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    raw_socket.bind((iface, 0))
    pkt = generate_arp_request_packet(target_ip, iface)
    raw_socket.send(pkt)
    raw_socket.settimeout(timeout)
    start = time.time()
    while True:
        try:
            recv_pkt = raw_socket.recv(65535)
            if recv_pkt[12:14] == b"\x08\x06":  # ARP
                eth_proto = struct.unpack("!H", recv_pkt[20:22])[0]
                if eth_proto == 2:  # ARP reply
                    recv_ip = socket.inet_ntoa(recv_pkt[28:32])
                    if recv_ip == target_ip:
                        raw_socket.close()
                        return True
        except socket.timeout:
            raw_socket.close()
            return False
        if time.time() - start > timeout:
            raw_socket.close()
            return False
