// Define LED pin

#define LED_PIN 2   // On-board LED is usually GPIO2


// L298N config for left side motor
#define ENB 19
#define IN4 18
#define IN3 5

// L298N config for right side motor
#define IN2 17
#define IN1 16
#define ENA 4


void setMotor(int motorL, int motorR) {
  // motorL and motorR range: -255 .. 255
  // negative = backward, positive = forward, 0 = stop

  // --- Left Motor ---
  if (motorL > 0) {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    ledcWrite(ENB, motorL);   // channel 0 for ENB
  } else if (motorL < 0) {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    ledcWrite(ENB, -motorL);  // take absolute value
  } else {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    ledcWrite(ENB, 0);
  }

  // --- Right Motor ---
  if (motorR > 0) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    ledcWrite(ENA, motorR);   // channel 1 for ENA
  } else if (motorR < 0) {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    ledcWrite(ENA, -motorR);
  } else {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    ledcWrite(ENA, 0);
  }
}

void setup_pin_for_L298N() {
  // Motor pins
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  ledcAttachChannel(ENB, 30000, 8, 0);
  ledcAttachChannel(ENA, 30000, 8, 1);

  // Configure PWM for ENA and ENB
  // ledcSetup(0, 1000, 8); // channel 0, 1kHz, 8-bit resolution
  // ledcAttachPin(ENB, 0); // left motor enable pin to channel 0
  // ledcSetup(1, 1000, 8); // channel 1, 1kHz, 8-bit resolution
  // ledcAttachPin(ENA, 1); // right motor enable pin to channel 1
}





void setup() {
  Serial.begin(115200);
  // Set pin as output
  pinMode(LED_PIN, OUTPUT);
  setup_pin_for_L298N();
}
  
void loop() {

  setMotor(255,255);
  delay(1000);
  setMotor(-255,-255);
  delay(1000);

  setMotor(0,0);
  delay(5000);

  // // Turn LED on
  // digitalWrite(LED_PIN, HIGH);
  // delay(100); // wait 1 second

  // // Turn LED off
  // digitalWrite(LED_PIN, LOW);
  // delay(100); // wait 1 second
}
