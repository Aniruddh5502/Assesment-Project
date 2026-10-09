## Design Approach
First I tried to map what things are needed to do and what components would I need to do that. Finalized on 3 components, 2 mock environments, one for computer control, and another for supplying the supply voltage/current simulation and ADC reading because of that. And then the MCU part. Which will work as the specimen that we actually want to build. 
## Implementation
I finalized the communication variations, what messages will be allowed to be sent as commands to do something or get some information. Finalized that it would need some functions to set the Threshold Voltage and another one for Threshold Current. Unless I wanted to merge them together which will be messy. I mean if for example say I need to update the threshold voltage then I cannot keep the current field empty, and vice versa. So I made them separate. Then comes the surge voltage and current simulation signal. The sketch/firmware inside the ESP32 detects that and decides if its upper than the threshold and if yes then what it should do with the  relay pin. And even if the surges later comes down, we don't actually turn the relay on for safety purposes. Only on human intervention it can be reset to High(connected) with the RESET command. And the initial stage was taken  as the relay was in HIGH(connected) stage.
Commands list are at:  README.md
## Results
The results I have deduced by testing our all the commands from the computer control. Sequentially:
- Set threshold values for Voltage and Current
- Check if each type of surge triggers the RELAY PIN flipping to LOW.\
- Tthen  comes the RESET PIN if it has been reset to HIGH
All these commands success are verified from the return messages they send. If they don't match we count them as failed test. Here is the result saved in a markdown file.

```markdown  
STARTING AUTOMATED TESTS

[STATUS] = [OK]
Command    :   THRESHOLD_VOLTAGE_120.00
Response   :   OK: Threshold Voltage updated

[STATUS] = [OK]
Command    :   THRESHOLD_CURRENT_1.000
Response   :   OK: Threshold Current updated

[STATUS] = [OK]
Command    :   ADC_READOUT_VOLTAGE_200.0
Response   :   FAULT: Voltage Surge Detected. Relay OFF

[STATUS] = [OK]
Command    :   ADC_READOUT_CURRENT_10.0
Response   :   FAULT: Over-current Detected. Relay OFF

[STATUS] = [OK]
Command    :   RESET_RELAY
Response   :   OK: Relay Reset Successful
```

