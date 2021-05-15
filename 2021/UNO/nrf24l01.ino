// Programming the Arduino UNO is similar to programming the Raspberry Pi.
// We will follow similar methods but with different programming language and steps.
// The steps will include the reading part of nRF24l01.
// The library for nRF24l01 for Arduino can be downloaded from github page. Start with including necessary libraries.
// We are using 16x2 LCD using I2C Shield so include Wire.h library and also the nRF24l01 is interfaced with SPI so include SPI library.

#include<SPI.h>
#include <Wire.h>

// Include RF24 and LCD library for accessing the RF24 and LCD functions.

#include<RF24.h>
#include <LiquidCrystal_I2C.h>

// The LCD address for I2C is 27 and it is a 16x2 LCD so write this into the function.

LiquidCrystal_I2C lcd(0x27, 16, 2);

// The RF24 is connected with standard SPI pins along with CE in pin 9 and CSN in pin 10.

RF24 radio(9, 10) ;

// Start the radio, set the power level and set channel to 76. Also set the pipe address same as Raspberry Pi and open the pipe to read.

radio.begin();
  radio.setPALevel(RF24_PA_MAX) ;
  radio.setChannel(0x76) ;
  const uint64_t pipe = 0xE0E0F1F1E0LL ;
  radio.openReadingPipe(1, pipe) ;

// Begin the I2C communication and initialise the LCD display.

Wire.begin();
  lcd.begin();
  lcd.home();
  lcd.print("Ready to Receive");

// Start listening to the radio for incoming messages and set the message length as 32 bytes.

radio.startListening() ;
  char receivedMessage[32] = {0}

// If radio is attached then start reading the message and save it.
// Print the message to serial monitor and also print to the display until the next message arrives.
// Stop the radio to listen and retry after some interval. Here it is 10 micro seconds.

if (radio.available()) {
    radio.read(receivedMessage, sizeof(receivedMessage));
    Serial.println(receivedMessage) ;
    Serial.println("Turning off the radio.") ;
    radio.stopListening() ;
    String stringMessage(receivedMessage) ;
    lcd.clear();
    delay(1000);
    lcd.print(stringMessage);
  }
