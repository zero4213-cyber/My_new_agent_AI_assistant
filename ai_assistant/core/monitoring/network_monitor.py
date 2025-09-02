# monitoring/network_monitor.py - giám sát bất thường mạng và kết nối đi

import os
import logging

from utils.error_logger import learn_from_failure

def monitor_network_anomalies():
    """Phát hiện các bất thường trên mạng bằng lệnh netstat."""
    try:
        result = os.popen("netstat -an").read()
        anomalies = [line for line in result.splitlines() if "ESTABLISHED" in line and "127.0.0.1" not in line]
        return anomalies[:10]
    except Exception as e:
        logging.error(f"Lỗi khi giám sát mạng: {e}")
        learn_from_failure("monitor_network_anomalies", e)
        return []

def monitor_outgoing_connections():
    """Kiểm tra các kết nối đi từ thiết bị hiện tại."""
    try:
        result = os.popen("netstat -n").read()
        connections = [line for line in result.splitlines() if "ESTABLISHED" in line]
        return connections[:10]
    except Exception as e:
        logging.error(f"Lỗi khi kiểm tra kết nối đi: {e}")
        learn_from_failure("monitor_outgoing_connections", e)
        return []