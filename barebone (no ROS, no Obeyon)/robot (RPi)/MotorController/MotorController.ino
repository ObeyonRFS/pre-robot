#include "motor_library.h"
#include <ArduinoJson.h>

// Define LED pin
#define LED_PIN 2   // On-board LED is usually GPIO2

#define LEFT_C1 13
#define LEFT_C2 12
#define LEFT_encoderA 13
#define LEFT_encoderB 12

volatile long left_encoder_count = 0;
unsigned long left_lastTime = 0;
float left_motorRPM = 0.0;

const int PPR = 360;

void IRAM_ATTR left_encoderISR(){
  if (digitalRead(LEFT_encoderB)==HIGH){
    left_encoder_count+=1;
  }else{
    left_encoder_count-=1;
  }
}


void setup() {
  Serial.begin(115200);
  // Set pin as output
  pinMode(LED_PIN, OUTPUT);
  pinMode(LEFT_encoderA, INPUT);
  pinMode(LEFT_encoderB, INPUT);

  attachInterrupt(digitalPinToInterrupt(LEFT_encoderA),left_encoderISR, RISING);

  setup_pin_for_L298N();

  left_lastTime=millis();
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
  //Receive command
  // static String input="";
  // while(Serial.available()){
  //   char c=(char)Serial.read();
  //   if (c=='\n'){
  //     processJson(input);
  //     input="";
  //   }else{
  //     input+=c;
  //   }
  // }

  //count PPR
  Serial.println(left_encoder_count);
  delay(100);


  //send motor speed
  // unsigned long currentTime = millis();
  // unsigned long dt = currentTime - left_lastTime;

  // if(dt>=100){//calculate every 100ms
  //   //Calculate speed in rpm
  //   long count;
  //   noInterrupts();
  //   count = left_encoder_count;
  //   left_encoder_count=0;
  //   interrupts();

  //   left_motorRPM = (count/(float)PPR) * (60000.0 / dt);

  //   Serial.print("Motor RPM: ");
  //   Serial.println(left_motorRPM);

  //   left_lastTime = currentTime;
  // }


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
