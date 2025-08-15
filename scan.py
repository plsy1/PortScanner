from arp import arp_ping
from concurrent.futures import ThreadPoolExecutor
import ipaddress
import socket


def scan_hosts(network_cidr, iface):
    """
    Scan a given IPv4 network for active hosts using ARP requests.

    Args:
        network_cidr (str): The target network in CIDR notation, e.g., "192.168.0.0/24".
        iface (str): Local network interface to send ARP requests from.

    Returns:
        list: A list of IP addresses (as strings) that responded to the ARP requests.
    """
    active_hosts = []

    def ping_ip(ip):
        if arp_ping(str(ip), iface=iface):
            print(f"{ip} ")
            active_hosts.append(str(ip))

    with ThreadPoolExecutor(max_workers=50) as executor:
        network = ipaddress.IPv4Network(network_cidr, strict=False)
        for ip in network.hosts():
            executor.submit(ping_ip, ip)
    return active_hosts


def scan_port(ip, port, timeout=1):
    """
    Check if a specific TCP port on a host is open.

    Args:
        ip (str): Target IP address.
        port (int): TCP port to scan.
        timeout (float): Connection timeout in seconds (default 1s).

    Returns:
        tuple: (port, bool) where bool is True if the port is open, False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((ip, port))
            return port, True
        except:
            return port, False

def scan_ports(ip, ports, max_threads=50):
    """
    Scan multiple TCP ports on a host concurrently.

    Args:
        ip (str): Target IP address.
        ports (iterable): List or range of TCP ports to scan.
        max_threads (int): Maximum number of concurrent threads (default 50).

    Returns:
        list: List of open TCP ports.
    """
    open_ports = []
    with ThreadPoolExecutor(max_threads) as executor:
        results = executor.map(lambda p: scan_port(ip, p), ports)
        for port, is_open in results:
            if is_open:
                open_ports.append(port)
    return open_ports