/***************************************************
 Camera Normalis – Arduino Audio Satellite
 ****************************************************/
#include "DFPlayerMini.h"

// Initialize the driver, passing the busy-wait method
DFPlayerMini SatellitePlayer;

long randNumber;

// DFPlayer pinout settings
static unsigned int PIN_BUSY = 4;
static unsigned int PIN_RX = 3;
static unsigned int PIN_TX = 2;

void setup()
{
  Serial.begin(115200);
  // Init the Random Seeder
  // randomSeed(analogRead(0));

  Serial.println(F("Init Player"));
  SatellitePlayer.init(PIN_BUSY, PIN_RX, PIN_TX);

  // Play introductory Fade-In Ambient Track (numbered as 01.mp3)
  Serial.println(F("Set Volume"));
  SatellitePlayer.setVolume(30);
  Serial.println(F("Play File 11"));

  SatellitePlayer.playFileAndWait(1);
}

void loop()
{
  // Random Ambient Track
  SatellitePlayer.setVolume(25);
  // SatellitePlayer.playFile(random(10, 21));
  SatellitePlayer.playFileAndWait(2);
  // Random Scene Track (if Lucky)
  //if (random(1, 11) > 7) {
  //  SatellitePlayer.setVolume(15);
  //  SatellitePlayer.playFile(random(20, 31));
  //}
}
