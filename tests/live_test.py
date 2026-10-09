import serial
import time
import sys
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown

console = Console()
root = Path(__file__).parent.parent

theme_char      =   "✽"
book_cloth      =   "#CC785C"
error           =   "#BF4D43"
focus           =   "#61AAF2"
white           =   "#FFFFFF"
black           =   "#000000"
cloud_light     =   "#BFBFBA"

class Test:
    def __init__(self, port='COM3', baudrate=115200):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
        except Exception as e:
            console.print(f"[{error}]ERROR: [/]{e}")
            sys.exit(1)
        
        # Give some time to setup the PORT    
        time.sleep(0.2)
        
        self.relay_state    =   "UNKNOWN"
        self.running        =   True

    def send_cmd(self, cmd:str, timeout:float=1.0)->str|None:
        """
        This function sends commands to change the threshold voltage and current
        and also send voltage reading mimicking the ADC input but here we shall simulate
        it with python USB C communication commands
        - THRESHOLD_VOLTAGE_120.00      sends signal to set the threshold voltage to 120.0V
        - THRESHOLD_CURRENT_10.000      sends signal to set the threshold current to 10.00A
        - ADC_READOUT_VOLTAGE_200.0     sends signal to mimic ADC reading VOLTAGE to send measured voltage is 200V
        - ADC_READOUT_CURRENT_10.0      sends signal to mimic ADC reading CURRENT to send measured current is 10.0A
        """
        # Send a command and return the reply line (or None on timeout)
        self.ser.reset_input_buffer()
        self.ser.write((cmd + "\n").encode())
        self.ser.flush()
        
        self.ser.timeout = timeout
        line = self.ser.readline()      # reads until "\n"
        
        if not line:
            return None
        return line.decode(errors="replace").strip()
    
    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
    
    def test_report(self):
        console.print(f"\n\n[{book_cloth}]      {theme_char} TEST SUITE    [/]")
        heading = "STARTING AUTOMATED TESTS"    
        
        # Test 1: Setting Threshold voltage to 120.0V
        command_1 = "THRESHOLD_VOLTAGE_120.00"
        test_1_response = self.send_cmd(command_1)
        test_1_status = False
        if test_1_response == "OK: Threshold Voltage updated":
            test_1_status = True
        if test_1_status:
            test_1_report = f"\n[STATUS] = [OK]\nCommand    :   {command_1}\nResponse   :   {test_1_response}"
        else:
            test_1_report = f"\n[STATUS] = [FAILED]\nCommand    :    {command_1}\nResponse    :    {test_1_response}"
        
 
        # Test 2: Setting Threshold current to 1.0A
        command_2 = "THRESHOLD_CURRENT_1.000"
        test_2_response = self.send_cmd(command_2)
        test_2_status = False
        if test_2_response == "OK: Threshold Current updated":
            test_2_status = True
        if test_2_status:
            test_2_report = f"\n[STATUS] = [OK]\nCommand    :   {command_2}\nResponse   :   {test_2_response}"
        else:
            test_2_report = f"\n[STATUS] = [FAILED]\nCommand    :    {command_2}\nResponse    :    {test_2_response}"            
 
        
        # Test 3: Surge within new limits VOLTAGE
        command_3 = "ADC_READOUT_VOLTAGE_200.0"
        test_3_response = self.send_cmd(command_3)
        test_3_status = False
        if test_3_response == "FAULT: Voltage Surge Detected. Relay OFF":
            test_3_status = True
        if test_3_status:
            test_3_report = f"\n[STATUS] = [OK]\nCommand    :   {command_3}\nResponse   :   {test_3_response}"
        else:
            test_3_report = f"\n[STATUS] = [FAILED]\nCommand    :    {command_3}\nResponse    :    {test_3_response}"            

        
        # Test 4: Surge within new limit CURRENT
        command_4 = "ADC_READOUT_CURRENT_10.0"
        test_4_response = self.send_cmd(command_4)
        test_4_status = False
        if test_4_response == "FAULT: Over-current Detected. Relay OFF":
            test_4_status = True
        if test_4_status:
            test_4_report = f"\n[STATUS] = [OK]\nCommand    :   {command_4}\nResponse   :   {test_4_response}"
        else:
            test_4_report = f"\n[STATUS] = [FAILED]\nCommand    :    {command_4}\nResponse    :    {test_4_response}"            
        
        
        # Test 5: Reset the Relay
        command_5 = "RESET_RELAY"
        test_5_response = self.send_cmd(command_5)
        test_5_status = False
        if test_5_response == "OK: Relay Reset Successful":
            test_5_status = True
        if test_5_status:
            test_5_report = f"\n[STATUS] = [OK]\nCommand    :   {command_5}\nResponse   :   {test_5_response}"
        else:
            test_5_report = f"\n[STATUS] = [FAILED]\nCommand    :    {command_5}\nResponse    :    {test_5_response}"            

        
        report = f"""
[{book_cloth}]{heading}[/]

[dim]{test_1_report}[/]
[dim]{test_2_report}[/]
[dim]{test_3_report}[/]
[dim]{test_4_report}[/]
[dim]{test_5_report}[/]
"""
        report_save = f"""
{heading}

{test_1_report}

{test_2_report}

{test_3_report}

{test_4_report}

{test_5_report}
"""
        
        
        # saving the report as a .md file in root / "tests" / "test_report.md"
        try:
            test_evidence = root / "test_evidence" / "test_log.md"
            with open(test_evidence, 'w', encoding='utf-8') as f:
                f.write(report_save)
            console.print(f"{report}")
            console.print(f"> [dim]Test Report Saved In : [/] [{book_cloth}] {test_evidence}[/]\n")
        except Exception as e:
            console.print(f"[dim]ERROR: [/] {e}\n")

        
        # Print the report in terminal
        console.print(f"{theme_char} [dim]Task Finished[/]\n")
