import serial
import time

class SerialBridge:
    def __init__(self, port='COM3', baudrate=115200):
        self.conn = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        self.conn.write(b"\r\n\r\n")
        time.sleep(2)
        self.conn.flushInput()

    def stream_command(self, gcode):
        if not gcode.strip():
            return
        
        full_command = (gcode.strip() + '\n').encode()
        self.conn.write(full_command)
        
        while True:
            response = self.conn.readline().decode().strip()
            if response == 'ok':
                return True
            if 'error' in response.lower():
                print(f"GRBL Error: {response}")
                return False

    def close(self):
        self.conn.close()
