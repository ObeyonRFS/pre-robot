#include "motor_library.h"
#include <ArduinoJson.h>

// Define LED pin
#define LED_PIN 2   // On-board LED is usually GPIO2



const int PPR = 2950;

#define LEFT_C1 13
#define LEFT_C2 12
#define LEFT_encoderA 13
#define LEFT_encoderB 12

volatile long left_encoder_count = 0;
unsigned long left_lastTime = 0;
float left_motorRPM = 0.0;


void IRAM_ATTR left_encoderISR(){
  if (digitalRead(LEFT_encoderB)==HIGH){
    left_encoder_count+=1;
  }else{
    left_encoder_count-=1;
  }
}


#define RIGHT_C1 14
#define RIGHT_C2 27
#define RIGHT_encoderA 14
#define RIGHT_encoderB 27

volatile long right_encoder_count = 0;
unsigned long right_lastTime = 0;
float right_motorRPM = 0.0;

void IRAM_ATTR right_encoderISR(){
  if (digitalRead(RIGHT_encoderB)==HIGH){
    right_encoder_count-=1;
  }else{
    right_encoder_count+=1;
  }
}



void setup() {
  Serial.begin(115200);
  // Set pin as output
  pinMode(LED_PIN, OUTPUT);
  pinMode(LEFT_encoderA, INPUT);
  pinMode(LEFT_encoderB, INPUT);
  attachInterrupt(digitalPinToInterrupt(LEFT_encoderA),left_encoderISR, RISING);
  pinMode(RIGHT_encoderA, INPUT);
  pinMode(RIGHT_encoderB, INPUT);
  attachInterrupt(digitalPinToInterrupt(RIGHT_encoderA),right_encoderISR, RISING);

  


  setup_pin_for_L298N();

  left_lastTime=millis();
  right_lastTime=millis();
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


  //send motor speed
  unsigned long currentTime = millis();
  unsigned long dt = currentTime - left_lastTime;

  if(dt>=100){//calculate every 100ms
    //Calculate speed in rpm
    long left_count;
    long right_count;
    noInterrupts();
    left_count = left_encoder_count;
    left_encoder_count=0;
    right_count = right_encoder_count;
    right_encoder_count=0;
    interrupts();

    left_motorRPM = (left_count/(float)PPR) * (60000.0 / dt);
    right_motorRPM = (right_count/(float)PPR) * (60000.0 / dt);


    Serial.print("Motor RPM: ");
    Serial.print(left_motorRPM);
    Serial.print(" ");
    Serial.println(right_motorRPM);

    left_lastTime = currentTime;
    right_lastTime = currentTime;

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
