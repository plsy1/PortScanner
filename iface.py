import socket
import struct
import fcntl


def get_default_iface_name():
    """
    Get the name of the default network interface (Linux).
    Reads /proc/net/route to find the interface with a default gateway.
    """
    with open("/proc/net/route") as f:
        for line in f.readlines()[1:]:
            parts = line.strip().split()
            iface, dest, _, flags, _, _, _, _, _, _, _ = parts[:11]
            if dest == "00000000" and int(flags, 16) & 2:  # flags 0x2 = UP
                return iface
    return None


def get_iface_info_by_name(ifname="eth0"):
    """
    Retrieve the IPv4 address and MAC address of a specified network interface.

    Parameters:
    -----------
    ifname : str, optional
        The name of the network interface (default is "eth0").

    Returns:
    --------
    tuple
        A tuple containing:
        - ip (str): The IPv4 address of the interface, e.g., "192.168.0.10".
        - mac (str): The MAC address of the interface in colon-separated format, e.g., "aa:bb:cc:dd:ee:ff".

    Notes:
    ------
    - This function uses low-level system calls (`ioctl`) via the `fcntl` and `socket` modules.
    - It works on Linux systems.
    - Requires read access to network interface information (no root privileges needed for reading).
    - Uses the following ioctl codes:
        - `SIOCGIFADDR (0x8915)` to get the IPv4 address.
        - `SIOCGIFHWADDR (0x8927)` to get the MAC address.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack("256s", ifname.encode("utf-8")[:15]),
    )[20:24]
    ip = socket.inet_ntoa(ip)

    mac = fcntl.ioctl(
        s.fileno(),
        0x8927,  # SIOCGIFHWADDR
        struct.pack("256s", ifname.encode("utf-8")[:15]),
    )[18:24]
    mac = ":".join("%02x" % b for b in mac)
    return ip, mac
