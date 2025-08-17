#include "motor_library.h"
#include <ArduinoJson.h>

// Define LED pin
#define LED_PIN 2   // On-board LED is usually GPIO2


void setup() {
  Serial.begin(115200);
  // Set pin as output
  pinMode(LED_PIN, OUTPUT);
  setup_pin_for_L298N();
}

void processJson(String &jsonString){
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, jsonString);

  if(error){
    Serial.print("JSON parse failed: ");
    Serial.println(error.c_str());
    return;
  }

  const char* command = doc["command"];
  if (strcmp(command, "set_motor_power")==0){
    int L=doc["parameters"]["L"];
    int R=doc["parameters"]["R"];
    setMotor(L,R);

    Serial.printf("Motor set -> L:%d  R:%d\n", L, R);
  }
}

  
void loop() {
  static String input="";

  while(Serial.available()){
    char c=(char)Serial.read();
    if (c=='\n'){
      processJson(input);
      input="";
    }else{
      input+=c;
    }
  }


  // setMotor(255,-255);
  // delay(1500);
  // setMotor(-255,255);
  // delay(1500);

  // setMotor(0,0);
  // delay(5000);

  // // Turn LED on
  // digitalWrite(LED_PIN, HIGH);
  // delay(100); // wait 1 second

  // // Turn LED off
  // digitalWrite(LED_PIN, LOW);
  // delay(100); // wait 1 second
}
