import subprocess
import os
import sys
from pathlib import Path

root = Path(__file__).parent.parent

class Esp:
    def __init__(self, firmware_folder, PORT="COM3" ,baud_rate=115200):
        self.firmware = root / f"{firmware_folder}"
        self.PORT = PORT
        self.baud_rate = baud_rate
        
    def compile(self):
        """This function compiles the firmware"""
        cmd = f"arduino-cli compile --fqbn esp32:esp32:esp32 {self.firmware}"
        response = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            shell=True,
        )
        return response
    
    def flash(self):
        """This function flashes the code to the board"""
        cmd = f"arduino-cli upload -p COM3 --fqbn esp32:esp32:esp32 {self.firmware}"
        response = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            shell=True,
        )
        return response
    