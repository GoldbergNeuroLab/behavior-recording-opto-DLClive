// the setup function runs once when you press reset or power the board

// upload this to arduino with IDE, take two signals from python using pyserial
// 'H' will turn laser on until 'L' is sent which will turn laser off
int laserPin = 13;
int incomingByte;       // a variable to read incoming serial data into

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  // initialize the LED pin as an output:
  pinMode(laserPin, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {


  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    }

    // if it's a capital H (ASCII 72), turn on the LED:
  if (incomingByte == 'H') {
     // pulse until receives next signal
    while (Serial.available() == 0) {
      digitalWrite(laserPin, HIGH);
      delay(5);
      digitalWrite(laserPin, LOW);
      delay(45);
      }
      incomingByte = Serial.read();
    }
    // if it's an L (ASCII 76) turn off the LED:
  if (incomingByte == 'L') {
    digitalWrite(laserPin, LOW);
    }


}
