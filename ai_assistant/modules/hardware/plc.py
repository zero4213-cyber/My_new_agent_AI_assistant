
def connect_plc(ip='192.168.0.1', port=502):
    try:
        from pyModbusTCP.client import ModbusClient
        plc = ModbusClient(host=ip, port=port, auto_open=True)
        return plc
    except Exception as e:
        return f"Lỗi kết nối PLC: {e}"
