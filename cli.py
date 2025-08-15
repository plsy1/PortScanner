from scan import *

def interactive_scan(network, iface, ports):
    """Interactive network host + port scan."""
    print(f"Using interface: {iface}")
    print(f"Scanning network {network} for active hosts...")
    active_hosts = scan_hosts(network, iface)

    if not active_hosts:
        print("No active hosts found. Exiting.")
        return

    print("\nActive hosts:")
    for idx, host in enumerate(active_hosts, 1):
        print(f"{idx}. {host}")

    # Let user select hosts
    selected = input(
        "\nEnter host numbers to scan ports (comma separated, e.g., 1,3): "
    )
    try:
        host_indices = [int(x.strip()) - 1 for x in selected.split(",")]
        hosts_to_scan = [active_hosts[i] for i in host_indices]
    except (IndexError, ValueError):
        print("Invalid input. Exiting.")
        return

    port_list = [int(p.strip()) for p in ports.split(",")]
    for host_ip in hosts_to_scan:
        print(f"\nScanning ports {port_list} on host {host_ip}...")
        open_ports = scan_ports(host_ip, port_list)
        print(f"Open ports on {host_ip}: {open_ports}")


def full_auto_scan(network, iface, ports):
    """Full automatic mode: scan all hosts on network + ports."""
    print(f"Full automatic scan on {network} using interface {iface}")
    active_hosts = scan_hosts(network, iface)
    if not active_hosts:
        print("No active hosts found. Exiting.")
        return

    port_list = [int(p.strip()) for p in ports.split(",")]
    for host_ip in active_hosts:
        print(f"\nScanning host {host_ip}...")
        open_ports = scan_ports(host_ip, port_list)
        print(f"Open ports on {host_ip}: {open_ports}")


def scan_single_ip(ip, port_range, threads=50):
    """Scan a single IP with a port range, e.g., 20-1024."""
    start_port, end_port = map(int, port_range.split("-"))
    ports = list(range(start_port, end_port + 1))
    print(f"Scanning {ip} ports {start_port}-{end_port}...")
    open_ports = scan_ports(ip, ports, max_threads=threads)
    print(f"Open ports on {ip}: {open_ports}")