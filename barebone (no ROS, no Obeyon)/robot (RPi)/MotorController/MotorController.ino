#include "motor_library.h"

// Define LED pin
#define LED_PIN 2   // On-board LED is usually GPIO2


void setup() {
  Serial.begin(115200);
  // Set pin as output
  pinMode(LED_PIN, OUTPUT);
  setup_pin_for_L298N();
}
  
void loop() {

  setMotor(255,-255);
  delay(1500);
  setMotor(-255,255);
  delay(1500);

  setMotor(0,0);
  delay(5000);

  // // Turn LED on
  // digitalWrite(LED_PIN, HIGH);
  // delay(100); // wait 1 second

  // // Turn LED off
  // digitalWrite(LED_PIN, LOW);
  // delay(100); // wait 1 second
}
