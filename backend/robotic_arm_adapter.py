import serial
import time
import json
from config import config_store

class RoboticArmAdapter:
    def __init__(self, port="COM3", baudrate=115200, mock=True):
        self.port = port
        self.baudrate = baudrate
        self.mock = mock
        self.connection = None
        if not self.mock:
            self._connect()

    def _connect(self):
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
        except Exception as e:
            print(f"Connection Failed: {e}")
            self.mock = True

    def send_gcode(self, gcode_list):
        results = []
        for line in gcode_list:
            if self.mock:
                results.append(f"MOCK_SEND: {line}")
            else:
                self.connection.write((line + "\n").encode())
                resp = self.connection.readline().decode().strip()
                results.append(resp)
        return results

    def execute_pattern_action(self, action_type, content):
        if action_type == "CANVAS_DRAW_FLOWCHART":
            gcode = ["G28", "G1 Z5 F500", "G1 X50 Y50 F3000", "G1 Z-1", "G1 X100 Y50", "G1 Z5"]
            return self.send_gcode(gcode)
        elif action_type == "BOARD_MATH_SOLVE":
            gcode = ["G1 X20 Y20 F3000", "G1 Z-1", "G1 X40 Y40", "G1 Z5"]
            return self.send_gcode(gcode)
        return []

arm_adapter = RoboticArmAdapter()