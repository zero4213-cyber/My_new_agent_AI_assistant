import random

# Mô phỏng hệ thống tường lửa đơn giản

def check_firewall_rules():
    rules = ["BLOCK_PORT_23", "ALLOW_PORT_443", "BLOCK_IP_192.168.1.10"]
    print("[Firewall] Đang kiểm tra các quy tắc:", rules)
    return rules

def simulate_intrusion_detection():
    alerts = [
        "[ALERT] Nghi ngờ truy cập từ IP lạ",
        "[ALERT] Cố gắng mở cổng bị chặn",
        "[INFO] Tất cả các quy tắc an toàn được tuân thủ"
    ]
    alert = random.choice(alerts)
    print(alert)
    return alert

def strengthen_firewall():
    print("[Firewall] Đã bật chế độ bảo vệ nâng cao.")
    return "Chế độ bảo vệ nâng cao đã được kích hoạt."

def protect_from_reverse_hack():
    print("[Firewall] Kích hoạt tường lửa chống mã độc tấn công ngược AI.")
    return "Tường lửa AI phòng chống tấn công ngược đã được kích hoạt."
