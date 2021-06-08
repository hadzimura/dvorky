/***************************************************
 Camera Normalis – Arduino Audio Satellite
 ****************************************************/

#include "Arduino.h"
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

// Initialize the driver, passing the busy-wait method
DFPlayerMini SatellitePlayer;


void printDetail(uint8_t type, int value);

void setup()
{
  mySoftwareSerial.begin(9600);
  Serial.begin(115200);
  
  Serial.println();
  Serial.println(F("Camera Normalis Audio Satellite"));
  Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));

  SatellitePlayer.init(pinBusy, pinReceive, pinTransmit, modifyVolume);
  SatellitePlayer.setVolume(15);

  // Ambient Tracks: 10-x
  static unsigned integer AmbientTracksStart = 10;
  static unsigned integer AmbientTracksStop = 20;

  // Scene Tracks: 50-x
  static unsigned integer SceneTracksStart = 50;
  static unsigned integer SceneTracksStop = 60;
  
  // SceneOpportunity rolls a dice 1-11 (10 shades) this number defines threshold for successful attempt  
  static unsigned integer SceneThreshold = 7;
  static unsigned integer SceneVolume = 15;


  // Play introductory Fade-In Ambient Track (numbered as 01.mp3)
  SatellitePlayer.playFile(1);
}

void loop()
{
  
  // Get number of a random Ambient Track (random max is exclusive so add 1)
  AmbientTrackNumber = random(AmbientTracksStart, AmbientTracksStop + 1);

  // Play Ambient Track (Volume changes via 'modifyVolume' callback below)  
  SatellitePlayer.playFile(AmbientTrackNumber);
  
  // When the Ambient Track finishes, roll a dice to determine if a Scene Track should play
  SceneOpportunity = random(1, 10);
  
  if (SceneOpportunity > SceneThreshold) {
    // Get number of a random Scene Track (random max is exclusive so add 1)
    SceneTrackNumber = random(SceneTracksStart, SceneTracksStop + 1);

    // The modifyVolume callback starts after 10 seconds so won't affect this
    SatellitePlayer.setVolume(SceneVolume);    
    SatellitePlayer.playFile(SceneTrackNumber);
  }
}

// Modify track volume using Fake Dice
void modifyVolume() {
  
  
}
