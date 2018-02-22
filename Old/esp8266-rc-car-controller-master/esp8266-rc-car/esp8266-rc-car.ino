#include <WiFiUdp.h>
#include <ESP8266WiFi.h>
#include<Servo.h>

#define m1 6  //Motor Driver Connection
#define m2 5  //Motor Driver Connection
#define ser 4 //Servo Motor Connection

Servo myservo;

const char* ssid = "Slyphen"; //Enter your wifi network SSID
const char* password = "12345678*"; //Enter your wifi network password

const int SERVER_PORT = 1111;
const int BAUD_RATE = 9600;

byte incomingByte = 0;

bool forwardsPressed = false;
bool backwardsPressed = false;
bool rightPressed = false;
bool leftPressed = false;

const int FORWARDS_PRESSED = 1;
const int FORWARDS_RELEASED = 2;
const int BACKWARDS_PRESSED = 3;
const int BACKWARDS_RELEASED = 4;
const int RIGHT_PRESSED = 5;
const int RIGHT_RELEASED = 6;
const int LEFT_PRESSED = 7;
const int LEFT_RELEASED = 8;

byte packetBuffer[512];

WiFiUDP Udp;


void connectWifi() {
  Serial.println();
  Serial.println();
  Serial.print("Connecting to WIFI network");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Udp.begin(SERVER_PORT);
}

void moveForwards() {
  Serial.println("Forwards");
  analogWrite(m1,150);
  analogWrite(m2,0);
}

void moveBackwards() {
  Serial.println("Backward");
  analogWrite(m1,0);
  analogWrite(m2,150);
}

void turnRight() {
  Serial.println("Right");
  myservo.write(180);
}

void turnLeft() {
  Serial.println("Left");
  myservo.write(120);
}

void turnforwardLeft() {
  Serial.println("Forward Left");
  analogWrite(m1,150);
  analogWrite(m2,0);
  myservo.write(120);
}

void turnforwardRight() {
  Serial.println("Forward Right");
  analogWrite(m1,150);
  analogWrite(m2,0);
  myservo.write(180);
}

void turnbackwardLeft() {
  Serial.println("Backward Left");
  analogWrite(m1,0);
  analogWrite(m2,150);
  myservo.write(120);
}

void turnbackwardRight() {
  Serial.println("Backward Right");
  analogWrite(m1,0);
  analogWrite(m2,150);
  myservo.write(180);
}

void resetSteering() {
  Serial.println("Reset Steering");
  myservo.write(150);
}

void resetEngine() {
  Serial.println("Reset Engine");
  analogWrite(m1,0);
  analogWrite(m2,0);
}

void detectKeyPresses() {
  if (incomingByte == FORWARDS_PRESSED) {
      forwardsPressed = true;
    }
    else if (incomingByte == BACKWARDS_PRESSED) {
      backwardsPressed = true;
    }

    if (incomingByte == FORWARDS_RELEASED) {
      forwardsPressed = false;
    }
    else if (incomingByte == BACKWARDS_RELEASED) {
      backwardsPressed = false;
    }

    if (incomingByte == RIGHT_PRESSED) {
      rightPressed = true;
    }
    else if (incomingByte == LEFT_PRESSED) {
      leftPressed = true;
    }

    if (incomingByte == RIGHT_RELEASED) {
      rightPressed = false;
    }
    else if (incomingByte == LEFT_RELEASED) {
      leftPressed = false;
    }
}

void handlePinOutputs() {
  while (forwardsPressed == true ) {
    moveForwards();
  }
  while (backwardsPressed == true) {
    moveBackwards();
  }
  while (backwardsPressed = false && forwardsPressed == false) {
    resetEngine();
  }
  while (rightPressed == true) {
    turnRight();
  }
  while (leftPressed == true) {
    turnLeft();
  }
  while (rightPressed == false && leftPressed == false){
    resetSteering();
  }
}

void setup() {
  Serial.begin(BAUD_RATE);
  delay(10);
  connectWifi();
  pinMode(ser,OUTPUT);
  pinMode(m1,OUTPUT);
  pinMode(m2,OUTPUT);
  myservo.attach(4);
  
}

void loop() {
  int noBytes = Udp.parsePacket();
  String received_command = "";

  if ( noBytes ) {
    Serial.print(millis() / 1000);
    Serial.print(":Packet of ");
    Serial.print(noBytes);
    Serial.print(" received from ");
    Serial.print(Udp.remoteIP());
    Serial.print(":");
    Serial.println(Udp.remotePort());

    Udp.read(packetBuffer,noBytes);
    Serial.println();

    Serial.println(packetBuffer[0]);
    incomingByte = packetBuffer[0];
    Serial.println();
  }
  detectKeyPresses();
  handlePinOutputs();
}
