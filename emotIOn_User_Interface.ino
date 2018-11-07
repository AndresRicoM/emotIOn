/*

  ███████╗███╗   ███╗ ██████╗ ████████╗   ██╗ ██████╗       ███╗   ██╗
  ██╔════╝████╗ ████║██╔═══██╗╚══██╔══╝   ██║██╔═══██╗      ████╗  ██║
  █████╗  ██╔████╔██║██║   ██║   ██║█████╗██║██║   ██║█████╗██╔██╗ ██║
  ██╔══╝  ██║╚██╔╝██║██║   ██║   ██║╚════╝██║██║   ██║╚════╝██║╚██╗██║
  ███████╗██║ ╚═╝ ██║╚██████╔╝   ██║      ██║╚██████╔╝      ██║ ╚████║
  ╚══════╝╚═╝     ╚═╝ ╚═════╝    ╚═╝      ╚═╝ ╚═════╝       ╚═╝  ╚═══╝

  Main code for emotIOn tracking device.
  This device is in charge of:
  - Light animation for selecting emotional states.
  - UDP communication with terMITe.
  - Saving data on SD Card.

  Andres Rico - 2018

*/

#include <Adafruit_NeoPixel.h> //NoePixel ring operation libraries. 
#ifdef __AVR__
#include <avr/power.h>
#endif
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <SPI.h> //Include libraries for communication with an SD card.
#include <SD.h>
#include <TimeLib.h>


#define PIN D8 //Pin for controlling ring colors.
#define CS_PIN 4 //Pin for communication with SD Card

File myFile; //Declare file object for using SD library fucntions.

Adafruit_NeoPixel strip = Adafruit_NeoPixel(8, PIN, NEO_GRB + NEO_KHZ800);//Create object for controlling lights.

char ssid[] = "";  //Internet credentials
char pass[] = ""; 

WiFiUDP Udp; //UDP communication variables
unsigned int port = 5514;
char packet[255];

int potentiometerpin = A0; //Potentiometer variables and input pin
int resistance;
int pot_state;

String pack; //Udp receiving string
String current_emotion, current_data, data2write; //Construction strings for writing SD card

void setup() {
  Serial.begin(115200); //Begin Serial
  strip.begin(); //Begin LED strip control.CMD
  
  strip.show(); //Reset LED Strip

  WiFi.begin(ssid, pass); //Begin WiFi connection.
  while (WiFi.status() != WL_CONNECTED) {
    readytogo();
    Serial.print(".");
  }

  Serial.println("Connection Successful");
  Udp.begin(port);
  Serial.printf("My IP Address is IP %s, at port %d\n", WiFi.localIP().toString().c_str(), port); //Print IP adress for control unit.

  Serial.println("Initializing SD card...");

  if (!SD.begin(CS_PIN)) {
    Serial.println("SD initialization has failed");
    return;
  }
  Serial.println("SD initialization done!");

  myFile = SD.open("mydata.txt", FILE_WRITE); //Open file for writing sensor data.

  for (int i = 0; i < 5; i++) { //3 Green flashes of the LED ring
    turncolor(0,255,0);
    delay(100);
    turncolor(0,0,0);
    delay(100);
  }
  stripoff();

  Serial.println("Ready to Start!");
}

void loop() {
  getres();
  getstate();
  if (true/*timeStatus() != timeNotSet*/) {
    if (true/*now() != prevDisplay*/) { //Write new Data
      terMITedata();
      setemotion();
      data2write = current_data + " , " + current_emotion;
      Serial.println(data2write);
      sdwrite();
    }
  }
}

void turncolor(unsigned int r, unsigned int g, unsigned int b) {
  for (int i = 0; i < 8; i++) {
    strip.setPixelColor(i, r, g, b);
    delay(15);
  }
  strip.show();
}

void stripoff() { //Funtion for turning lights off. 
  for (int i = 0; i < 8; i++) {
    strip.setPixelColor(i, 0, 0, 0);
    delay(15);
  }
  strip.show();
}

void getres() { //Gets resistance value from potentiometer (0 - 1028)
  resistance = analogRead(potentiometerpin);
  //Serial.println(resistance);
}

void getstate() { //Function for setting state variables (0-1) and turning LEDs into state color dependent on resistance value from potentiometer indicating individual emotions. 
  if (resistance < 256) {
    pot_state = 0;
    turncolor(255, 0, 0); //RED - Anger
  }
  if ((resistance >= 256) & (resistance < (256 * 2))) {
    pot_state = 1;
    turncolor(255, 255, 0); //YELLOW - Joy
  }
  if ((resistance >= (256 * 2)) & (resistance < (256 * 3))) {
    pot_state = 2; 
    turncolor(0, 50, 255);//BLUE - Sadness
  }
  if ((resistance >= (256 * 3)) & (resistance < (256 * 4))) {
    pot_state = 3;
    turncolor(255, 0, 255);//PINK - Disgust
  }
}

void readytogo() { //LED loading function. Pulses white. 
  for (int color = 0; color < 255; color++) {
    for (int led = 0; led < 8; led++) {
      strip.setPixelColor(led, color, color, color);
      delay(1);
    }
    strip.show();
  }
  for (int color = 0; color < 255; color++ ) {
    for (int led = 0; led < 8; led++) {
      strip.setPixelColor(led, (255 - color), (255 - color), (255 - color));
      delay(1);
    }
    strip.show();
  }
}

void terMITedata() { //UDP request to terMITe for data
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    int len = Udp.read(packet, 255);
    if (len > 0) {
      packet[len] = 0;
    }
    pack = String(packet); 
    Serial.println(pack);
    current_data = pack; //Assigns terMITe data to current_data variable for writing it into the SD. 
  }
}

void sdwrite() { //Function for writing data sring into SD card file. 
  myFile = SD.open("mydata.txt", FILE_WRITE);
  if (myFile) {
    Serial.print("Writing sensor data...");
    myFile.println(data2write);
    myFile.close();
    Serial.println("done.");
  } else {
    // if the file didn't open, print an error:
    Serial.println("Error writing sensor data");
  }
}

void setemotion() { //Sets emotion variable depending on potentiometers position. 
  switch (pot_state) {
    case 0: //Anger
      Serial.println("Anger");
      current_emotion = "1";
      break;
    case 1: //Joy
      Serial.println("Joy");
      current_emotion = "2";
      break;
    case 2: //Fear
      Serial.println("Sadness");
      current_emotion = "3";
      break;
    case 3: //Sadness
      Serial.println("Disgust");
      current_emotion = "4";
      break;
  }
}

