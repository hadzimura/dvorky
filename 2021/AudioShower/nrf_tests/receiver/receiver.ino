/*
* Arduino Wireless Communication Tutorial
*       Example 1 - Receiver Code
*
* by Dejan Nedelkovski, www.HowToMechatronics.com
*
* Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
*/
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "printf.h"

RF24 radio(9, 10); // CE, CSN
const byte address[6] = "00001";

void setup() {
  Serial.begin(115200);
  if (!radio.begin()) {
    Serial.println(F("radio hardware is not responding!!"));
    while (1) {} // hold in infinite loop
  }
  //radio.setChannel(76);
  //radio.setPALevel(RF24_PA_LOW);     // RF24_PA_MAX is default.
  radio.openReadingPipe(0, address);
  radio.startListening();

  printf_begin();             // needed only once for printing details
  // radio.printDetails();       // (smaller) function that prints raw register values
  radio.printPrettyDetails(); // (larger) function that prints human readable data
}
void loop() {
  Serial.println(F("Reading..."));
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));
    Serial.println(text);
  } else {
    Serial.println(F("Nothing received..."));
    delay(1000);
    }
}
