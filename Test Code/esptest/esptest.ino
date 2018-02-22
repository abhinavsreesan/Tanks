//TANKS MARK 2.0

#include <WiFiUdp.h>
#include <ESP8266WiFi.h>

#define m1 D1 
#define m2 D2 
#define m3 D3 
#define m4 D4 
#define b1 D5//button

const char* ssid = "Oneplus"; //Enter your wifi network SSID
const char* password = "12345678"; //Enter your wifi network password


const int SERVER_PORT = 1111;
const int BAUD_RATE = 115200;

byte incomingByte = 0;

bool lforwardsPressed = false;
bool lbackwardsPressed = false;
bool rforwardsPressed = false;
bool rbackwardsPressed = false;
bool buttonPressed = false;

const int RFORWARDS_PRESSED = 1;
const int RFORWARDS_RELEASED = 2;
const int LBACKWARDS_PRESSED = 3;
const int LBACKWARDS_RELEASED =4;
const int RBACKWARDS_PRESSED = 5;
const int RBACKWARDS_RELEASED =6;
const int LFORWARDS_PRESSED = 7;
const int LFORWARDS_RELEASED = 8;
const int BUTTON_PRESSED = 9;
const char BUTTON_RELEASED = 0;


byte packetBuffer[512];

WiFiUDP Udp;
IPAddress ip;  


void initOutputs() {
  pinMode(m1,OUTPUT);
  pinMode(m2,OUTPUT);
  pinMode(m3,OUTPUT);
  pinMode(m4,OUTPUT);
  pinMode(b1,OUTPUT);
  digitalWrite(b1,LOW);
}

void connectWifi() {
  Serial.println();
  Serial.println();
  Serial.print("Connecting to WIFI network");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Udp.begin(SERVER_PORT);
  ip = WiFi.localIP();
  Serial.println(ip);

}

void moveLForwards() {
  Serial.println("Left Forward");
  analogWrite(m1,1024);
  analogWrite(m2,0);
}

void moveRForwards() {
  Serial.println("Right Forward");
  analogWrite(m3,1024);
  analogWrite(m4,0);
}

void moveLBackwards() {
  Serial.println("Left Backwards");
  analogWrite(m1,0);
  analogWrite(m2,1024);
}

void moveRBackwards() {
  Serial.println("Right Backwards");
  analogWrite(m3,0);
  analogWrite(m4,1024);
}

void resetLEngine()
{
  Serial.println("L Reset");
  analogWrite(m1,0);
  analogWrite(m2,0);
}

void resetREngine()
{
  Serial.println("R Reset");
  analogWrite(m3,0);
  analogWrite(m4,0);
}
void gunControl() {
  Serial.println("Button On");
  digitalWrite(b1,HIGH);
}

void gunReset(){
  Serial.println("Button Off");
  digitalWrite(b1,LOW);
}


void resetEngine() {
  Serial.println("reset e");
  analogWrite(m1,0);
  analogWrite(m2,0);
}

void detectKeyPresses() {
  if (incomingByte == LFORWARDS_PRESSED) {
      lforwardsPressed = true;
    }
    else if (incomingByte == LBACKWARDS_PRESSED) {
      lbackwardsPressed = true;
    }

    if (incomingByte == LFORWARDS_RELEASED) {
      lforwardsPressed = false;
    }
    else if (incomingByte == LBACKWARDS_RELEASED) {
      lbackwardsPressed = false;
    }
     if (incomingByte == RFORWARDS_PRESSED) {
      rforwardsPressed = true;
    }
    else if (incomingByte == RBACKWARDS_PRESSED) {
      rbackwardsPressed = true;
    }

    if (incomingByte == RFORWARDS_RELEASED) {
      rforwardsPressed = false;
    }
    else if (incomingByte == RBACKWARDS_RELEASED) {
      rbackwardsPressed = false;
    }

    if (incomingByte == BUTTON_PRESSED) {
      buttonPressed = true;
    }
    else if (incomingByte == BUTTON_RELEASED) {
      buttonPressed = false;
    }
}

void handlePinOutputs() {
  if (rforwardsPressed == true) {
    moveRForwards();
  }
  else if (rbackwardsPressed == true) {
    moveRBackwards();
  }
  else {
    resetREngine();
  }
   
   if (lforwardsPressed == true) {
    moveLForwards();
  }
  else if (lbackwardsPressed == true) {
    moveLBackwards();
  }
  else {
    resetLEngine();
  }
  if(buttonPressed == true) {
    gunControl();
  }
  else if(buttonPressed == false) {
    gunReset();
  }
}

void setup() {
  Serial.begin(BAUD_RATE);
  delay(10);
  initOutputs();
  connectWifi();
}

void loop() {
  int noBytes = Udp.parsePacket();
  String received_command = "";
  if ( noBytes ) 
  {
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

    detectKeyPresses();
    handlePinOutputs();
  }
  
}
