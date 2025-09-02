# tools/network_scanner.py - quét cổng đang mở trên thiết bị hoặc IP

import socket

def scan_open_ports(ip, ports=range(20, 1025), timeout=0.5):
    """Quét các cổng mở từ dải ports trên IP cho trước."""
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception:
            continue
    return open_ports or ["Không phát hiện cổng mở."]