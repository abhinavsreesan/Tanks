//LASER TAG MARK 7.0
/*
  *CONNECTIONS
   
  TRIGGER-A0
  Receive-pin 2
  Transmit-pin 3
  Buzzer-A1

  *LCD DISPLAY
  
  VSS-gnd
  VDD-5V
  VEE-gnd
  RS pin-12
  Enablepin-11
  D4 pin-7
  D5 pin-8
  D6 pin-9
  D7 pin-10
  R/W-GND
  led+&- to +5V and ground
  
*/

#include <IRLib.h>
#include <EEPROM.h>
#define btnAddr 0
#define dthAddr 1
#include <LiquidCrystal.h>
/***********************************************************************************************************************************************/

#define btn 6
#define buzz 4
#define rumble 5

/***********************************************************************************************************************************************/
int rumble_time = 0;
int RECV_PIN = 2;
int flag = 0;
int btncnt = 0; //no. of bullets
int read2 = 0;
long time = 0;
int read;
int disableSend = 0;
long l = 0;
long debounce = 200;
int dth = 0;
int led = 1;
long t1 = 0;
int t3 = 0;
int flag1 = 0;
int oldValue = 0;
int ttime = 0;
int flag2=0;
/***********************************************************************************************************************************************/
IRrecv My_Receiver(RECV_PIN);
IRsend My_Sender;
LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

IRdecode My_Decoder;
unsigned int Buffer[RAWBUF];

/***********************************************************************************************************************************************/

  void setup()
{
  Serial.begin(9600);

  //LCD
  lcd.begin(16, 2);

  //Rumble
  pinMode(rumble, OUTPUT);
  digitalWrite(rumble, LOW);
  dth=EEPROM.read(dthAddr);
  btncnt=EEPROM.read(btnAddr);

  //trigger
  pinMode(btn, INPUT_PULLUP);
  pinMode(buzz, OUTPUT);
  digitalWrite(buzz, LOW);
  digitalWrite(btn, HIGH);
  //oldValue = analogRead(ldrPin);
  My_Receiver.enableIRIn(); // Start the receiver
  My_Decoder.UseExtnBuf(Buffer);
}

/***********************************************************************************************************************************************/

//Receiver code
    void checkForInput() 
  {
  if (My_Receiver.GetResults(&My_Decoder)) 
  {
    My_Decoder.decode();
    TIMSK2 = 0;
    //Value
      //Serial.println("inside receiver loop");
      //Serial.println(My_Decoder.value, HEX);
      if(My_Decoder.value == 29986)
      {
        EEPROM.write(btnAddr,0);
        EEPROM.write(dthAddr,0);
        btncnt=EEPROM.read(btnAddr);
        dth=EEPROM.read(dthAddr);
      }
    if (My_Decoder.value == 3021 && dth <= 20)
    {
      dth++;
      EEPROM.write(dthAddr,dth);
      digitalWrite(buzz, HIGH);
      delay(200);           //500 se change kiya
      digitalWrite(buzz, LOW);
      Serial.println("inside receiver loop right");
      Serial.println(My_Decoder.value, HEX);
      delay(100);
    }
    My_Receiver.resume();
    My_Receiver.enableIRIn();
    //  My_Receiver.resume();
  }
}

/***********************************************************************************************************************************************/

  void loop()
{ 
  if (dth <= 20)
  {
    lcd.setCursor(4, 0);
    lcd.print("RED TEAM");
    
    lcd.setCursor(0, 1);
    lcd.print("AMMO:");
    lcd.setCursor(5, 1);
    if ((500 - btncnt) >= 100)
    {
      lcd.print((500 - btncnt));
      //Serial.println((500 - btncnt));
    }
    else if ((500 - btncnt) >= 10 && (500 - btncnt) <100)
    { lcd.print("0");
      lcd.setCursor(6, 1);
      lcd.print((500 - btncnt));
    }
    else if ((500 - btncnt) < 10)
    {
      lcd.setCursor(5,1);
      lcd.print("00");
      lcd.setCursor(7, 1);
      lcd.print((500 - btncnt));
    }
    
    lcd.setCursor(9, 1);
    lcd.print("LIFE:");
    
    lcd.setCursor(14, 1);
    if ((20 - dth) >= 10)
    {
      lcd.print((20 - dth));
    }
    else if ((20 - dth) < 10 && (20 - dth)>=0)
    {
      lcd.print("0");
      lcd.setCursor(15, 1);
      lcd.print((20 - dth));
    }
  }
  if (dth >= 20)
  {
    flag2 = 1;
  }

 //button read code
  read = digitalRead(btn);
  //Serial.println(read);
  if (read == HIGH && millis() - time > debounce)
  { 
    Serial.println("DATA SEND");
    
    //if(!disableSend)
    if (btncnt <= 500 && flag1==0)
    {
      //Serial.println("send loop");
      My_Sender.send(RC5, 0xbcb, 20); //data to be sent
      digitalWrite(rumble, HIGH);
      Serial.println("SEND DATA");
      rumble_time = millis();
      btncnt++;
      EEPROM.write(btnAddr,btncnt);
      if(btncnt>=500)
      {
        flag1=1;
      }
    }
    My_Receiver.enableIRIn();
    checkForInput();
    My_Receiver.enableIRIn();
    time = millis();
    if (flag1 == 1 || flag2==1)
    { 
      lcd.clear();
      lcd.setCursor(2,0);
      lcd.print("GAME OVER!!!");//end of life
      digitalWrite(buzz,HIGH);
      digitalWrite(rumble,HIGH);
      //delay(10000);
    }
  }
  checkForInput();
  ttime = millis() - rumble_time;//rumble motor time

  //Serial.println(ttime);
  if ((ttime) > 100)
  {
    digitalWrite(rumble, LOW);
  }

}
