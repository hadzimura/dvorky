/***************************************************
 Camera Normalis – Arduino Audio Satellite
 ****************************************************/
#include "DFPlayerMini.h"

// Initialize the driver, passing the busy-wait method
DFPlayerMini SatellitePlayer;

long randNumber;

// DFPlayer pinout settings
static unsigned int PIN_BUSY = 10;
static unsigned int PIN_RX = 10;
static unsigned int PIN_TX = 10;

void setup()
{
  // Init the Random Seeder
  randomSeed(analogRead(0));
  
  SatellitePlayer.init(PIN_BUSY, PIN_RX, PIN_TX, modifyVolume);

  // Play introductory Fade-In Ambient Track (numbered as 01.mp3)
  SatellitePlayer.setVolume(15);
  SatellitePlayer.playFile(1);
}

void loop()
{
  // Random Ambient Track
  SatellitePlayer.setVolume(15);
  SatellitePlayer.playFile(random(10, 21));

  // Random Scene Track (if Lucky)
  if (random(1, 11) > 7) {
    SatellitePlayer.setVolume(15);
    SatellitePlayer.playFile(random(20, 31));
  }
}
