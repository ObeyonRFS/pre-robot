// Define LED pin

#define LED_PIN 2   // On-board LED is usually GPIO2



void setup() {
  // Set pin as output
  pinMode(LED_PIN, OUTPUT);
}
  
void loop() {

  // Turn LED on
  digitalWrite(LED_PIN, HIGH);
  delay(100); // wait 1 second

  // Turn LED off
  digitalWrite(LED_PIN, LOW);
  delay(100); // wait 1 second
}
