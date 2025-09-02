
from modules.hardware.arduino import connect_arduino
from modules.hardware.plc import connect_plc
from modules.hardware.camera import capture_and_process

def handle_hardware_command(command: str):
    command = command.lower()
    if "arduino" in command:
        return connect_arduino()
    elif "plc" in command:
        return connect_plc()
    elif "camera" in command:
        return capture_and_process()
    return "Không nhận diện được lệnh phần cứng."
