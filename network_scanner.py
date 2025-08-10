import subprocess
import socket
from ipaddress import IPv4Network
import platform

def ping(host: str) -> bool:
    """
    Ping a host to check if it's online.
    Works on Windows and Unix-based systems.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    print(f"Pinging {host}...")
    result = subprocess.run(command, stdout=subprocess.DEVNULL)
    return result.returncode == 0

def scan_ports(ip: str, ports: list[int]) -> list[int]:
    """
    Scan a list of ports on the given IP.
    Returns a list of open ports.
    """
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            try:
                if sock.connect_ex((ip, port)) == 0:
                    open_ports.append(port)
            except Exception:
                pass
    return open_ports

def main():
    # Update this to your actual subnet (find via ipconfig)
    subnet = '.....'  

    ports_to_scan = [
        20, 21, 22, 23, 25, 53, 80, 110, 111, 135,
        139, 143, 161, 162, 389, 443, 445, 465, 587,
        636, 993, 995, 1433, 1521, 1723, 3306, 3389,
        5900, 8080, 8443
    ]

    print(f"Starting network scan on subnet: {subnet}\n")

    network = IPv4Network(subnet)
    active_hosts = []

    for ip in network.hosts():
        ip_str = str(ip)
        if ping(ip_str):
            open_ports = scan_ports(ip_str, ports_to_scan)
            active_hosts.append((ip_str, open_ports))

    if active_hosts:
        print(f"\nFound {len(active_hosts)} active device(s):\n")
        for ip, ports in active_hosts:
            if ports:
                ports_str = ', '.join(str(p) for p in ports)
                print(f"{ip} - Open ports: {ports_str}")
            else:
                print(f"{ip} - No common open ports found")
    else:
        print("No active devices found.")

if __name__ == "__main__":
    main()