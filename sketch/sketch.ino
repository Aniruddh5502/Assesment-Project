#include <Arduino.h>

#define PIN_RELAY 5

// setting the current and voltage threshold to 220V and 1A
float THRESHOLD_VOLTAGE     =   220;
float THRESHOLD_CURRENT     =   1;
float ADC_READING_VOLTAGE   =   0;
float ADC_READING_CURRENT   =   0;

String input = "";

void setup(){
    pinMode(PIN_RELAY, OUTPUT);
    digitalWrite(PIN_RELAY, HIGH);      //  indicating the relay is connected
    Serial.begin(115200);
}

void loop(){
    // read one character at a time
    while(Serial.available()){
        char c = Serial.read();

        if (c=='\n'){
            input.trim();
            handle_command(input);
            input = "";
        }else{
            input += c;
            if (input.length() > 64) input = ""; //safety
        }
    }
}

void handle_command(String cmd){

    // if the command is ping
    if(cmd.startsWith("THRESHOLD_VOLTAGE_")){
        String value_str = cmd.substring(18);
        THRESHOLD_VOLTAGE = value_str.toFloat();
        Serial.println("OK: Threshold Voltage updated");
    
    }else if(cmd.startsWith("THRESHOLD_CURRENT_")){
        // extract value after the prefix
        String value_str = cmd.substring(18);
        THRESHOLD_CURRENT = value_str.toFloat();
        Serial.println("OK: Threshold Current updated");
    
    }else if(cmd.startsWith("ADC_READOUT_VOLTAGE_")){
        // checking if the voltage triggers relay switch
        String value_str = cmd.substring(20);
        ADC_READING_VOLTAGE = value_str.toFloat();
        
        // comparing the voltage to the threshold
        if(ADC_READING_VOLTAGE > THRESHOLD_VOLTAGE){
            // now we turn off the relay setting the pin to LOW
            digitalWrite(PIN_RELAY, LOW);
            Serial.println("FAULT: Voltage Surge Detected. Relay OFF");
        }
        /*
        here we are setting the replay disconnected when the ADC reading is higher than
        the threshold voltage, But if its lower than the threshold voltage and the relay pin 
        is already low and it was at HIGH position at the start that means it was 
        previously flipped to low because of voltage surge. so we keep a manual RESET 
        option to make it start running again.
        */
    
    }else if(cmd.startsWith("ADC_READOUT_CURRENT_")){
        // checking if the current triggers relay switch
        String value_str = cmd.substring(20);
        ADC_READING_CURRENT = value_str.toFloat();

        // comparing the current to threshold
        if(ADC_READING_CURRENT > THRESHOLD_CURRENT){
            // now we turn on the relay setting the pin to LOW
            digitalWrite(PIN_RELAY, LOW);
            Serial.println("FAULT: Over-current Detected. Relay OFF");
        }
    }else if(cmd == "RESET_RELAY"){
        // Here we reset the relay state to HIGH
        digitalWrite(PIN_RELAY, HIGH);
        Serial.println("OK: Relay Reset Successful");
    }
}