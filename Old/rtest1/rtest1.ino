#include <IRLib.h>

int RECV_PIN = 2;
int btn=5;
long debounce=200;
int read=0;
int time=0;

IRrecv My_Receiver(RECV_PIN);
IRsend My_Sender;

IRdecode My_Decoder;
unsigned int Buffer[RAWBUF];

void setup()
{
  Serial.begin(9600);
  pinMode(btn,INPUT);
  My_Receiver.enableIRIn(); // Start the receiver
  My_Decoder.UseExtnBuf(Buffer);
}

void checkForInput(){
    if (My_Receiver.GetResults(&My_Decoder)) {
    //Restart the receiver so it can be capturing another code
    //while we are working on decoding this one.
     
    My_Decoder.decode();
    TIMSK2 = 0;  
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

    read=digitalRead(btn);
    if(read==HIGH && millis()-time > debounce)
    {
    Serial.println("send loop");
    //send a code  every time a character is received from the serial port
    //Sony DVD power A8BCA
    My_Sender.send(RC5,0xa8bcd, 20);
    
    My_Receiver.enableIRIn();
    checkForInput();
    My_Receiver.enableIRIn();
    time=millis();
  }
  checkForInput();
  
}
