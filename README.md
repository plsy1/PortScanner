# **PortScanner**

A **Python-based command-line tool** for scanning active hosts on a local network and checking open ports. Supports both interactive and full-automatic modes.

## **Features**

- Discover active hosts on a LAN using **ARP ping**.
- Scan specified ports on selected hosts.
- Fully automatic mode to scan all hosts and ports without interaction.
- Specify a single IP and port range for targeted scanning.
- Multi-threaded scanning for faster results.
- Cross-platform (Linux/macOS) via raw socket and standard Python libraries.

## **Requirements**

- Python 3.6+
- Linux/macOS (requires raw socket permissions for ARP scanning)
- No external libraries required for scanning; only standard Python modules.

## **Usage**

```
python3 main.py [options]
```

### **Options**

| **Flag**      | **Description**                                              |
| ------------- | ------------------------------------------------------------ |
| -n, --network | Target network in CIDR format, e.g., 192.168.0.0/24          |
| -p, --ports   | Comma-separated list of ports to scan, e.g., 22,80,443       |
| -i, --iface   | Network interface to use, e.g., eth0                         |
| --ip          | Scan a single host IP instead of the full network            |
| --port-range  | Port range to scan, e.g., 20-1024                            |
| --threads     | Maximum concurrent threads (default: 50)                     |
| --all         | Full automatic mode: scan all hosts and selected ports without interaction |

### **Examples**

- **Interactive network scan:**

```
python3 main.py -n 192.168.0.0/24 -p 22,80,443
```

- **Full automatic scan:**

```
python3 main.py -n 192.168.0.0/24 -p 22,80,443 --all
```

- **Single host port range scan:**

```
python3 main.py --ip 192.168.0.101 --port-range 20-1024
```



