//For Blue Tank

#include <IRLib.h>
#include <EEPROM.h>

#define hltAddr 0
#define buzz A1

int RECV_PIN = 2;
int btn=A0;
int hlt=0; //Setting initial health to zero.
long debounce=200;
int read;
int time=0;


IRrecv My_Receiver(RECV_PIN);
IRsend My_Sender;

IRdecode My_Decoder;
unsigned int Buffer[RAWBUF];

void setup()
{
  pinMode(buzz, OUTPUT);
  digitalWrite(buzz, LOW);
  for(int i=4;i<9;i++)
  {
    pinMode(i,OUTPUT);
    digitalWrite(i,HIGH);
  }
  EEPROM.write(hltAddr,0);
  hlt=EEPROM.read(hltAddr);
  Serial.begin(9600);
  pinMode(btn,INPUT);
  My_Receiver.enableIRIn(); // Start the receiver
  My_Decoder.UseExtnBuf(Buffer);
}

void checkForInput(){
    if (My_Receiver.GetResults(&My_Decoder)) 
    {
      My_Decoder.decode();
      TIMSK2 = 0;  
     if (My_Decoder.value == 3019 && hlt <= 10)
    {
      hlt++;
      EEPROM.write(hltAddr,hlt);
      digitalWrite(hlt+3,LOW); 
      digitalWrite(buzz, HIGH);
      delay(200);//500 se change kiya
      digitalWrite(buzz, LOW);
      //Serial.println("inside receiver loop right");
      //Serial.println(My_Decoder.value, HEX);
      delay(100);
    }
    //My_Decoder.DumpResults();

    Serial.println("inside receiver loop");
    Serial.println(My_Decoder.value,HEX);
    delay(100); 
    My_Receiver.resume();
    My_Receiver.enableIRIn();
  //  My_Receiver.resume();
  }
  
  }
void loop() {
    //if (Serial.read() != -1) {
    read=digitalRead(btn);
    if(read==HIGH && millis()-time > debounce)
    {
      Serial.println("send loop");
      My_Sender.send(RC5,0xbcd, 20);
      My_Receiver.enableIRIn();
      checkForInput();
      My_Receiver.enableIRIn();
      time=millis();
  }
  checkForInput();
  if(hlt>= 10) 
  {
     digitalWrite(buzz,HIGH);
     for(int i=4;i<9;i++)
     {
      digitalWrite(i,HIGH);
      delay(500);
      digitalWrite(i,LOW);
     }
  }
  Serial.print("Health:");
  Serial.println(hlt);
  //delay(1000);
}
