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

// Ambient Tracks: 10-x
static unsigned int AmbientTracksStart = 10;
static unsigned int AmbientTracksStop = 20;
// Volume changes after 20 seconds
static unsigned int VolumeChangeMs = 20000;
static unsigned int AmbientVolume = 15;

// Scene Tracks: 50-x
static unsigned int SceneTracksStart = 50;
static unsigned int SceneTracksStop = 60;

// SceneOpportunity rolls a dice 1-11 (10 shades) this number defines threshold for successful attempt  
static unsigned int SceneThreshold = 7;
static unsigned int SceneVolume = 15;

void setup()
{
  // mySoftwareSerial.begin(9600);
  Serial.begin(115200);

  // Init the Random Seeder
  randomSeed(analogRead(0));
  
  Serial.println();
  Serial.println(F("Camera Normalis Audio Satellite"));
  Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));

  SatellitePlayer.init(PIN_BUSY, PIN_RX, PIN_TX, modifyVolume);
  SatellitePlayer.setVolume(15);


  // Play introductory Fade-In Ambient Track (numbered as 01.mp3)
  SatellitePlayer.playFile(1);
}

void loop()
{
  
  // Get number of a random Ambient Track (random max is exclusive so add 1)
  int AmbientTrackNumber = random(AmbientTracksStart, AmbientTracksStop + 1);

  // Play Ambient Track (Volume changes via 'modifyVolume' callback below) 
  SatellitePlayer.setVolume(AmbientVolume);
  // Reassign the AmbientVolume during callback (untested :)
  AmbientVolume = SatellitePlayer.playFile(AmbientTrackNumber);
  
  // When the Ambient Track finishes, roll a dice to determine if a Scene Track should play
  int SceneOpportunity = random(1, 10);
  
  if (SceneOpportunity > SceneThreshold) {
    // Get number of a random Scene Track (random max is exclusive so add 1)
    int SceneTrackNumber = random(SceneTracksStart, SceneTracksStop + 1);

    // The modifyVolume callback starts after 10 seconds so won't affect this
    SatellitePlayer.setVolume(SceneVolume);
    SatellitePlayer.playFile(SceneTrackNumber);
  }
}

// Modify track volume using Fake Dice
int modifyVolume() {

  // Set the Timer for a change of the volume    
  static unsigned long timer = millis();
  static unsigned int FakeDiceStep = 5;
  // Direction: 0: down, 1: up
  static unsigned int FakeDiceDirection = 0;  
  static unsigned int CurrentVolume = AmbientVolume;
  

  // Timer for the Volume change reached?
  if (millis() - timer > VolumeChangeMs) {
    
    // Fake Dice Lite
    // 0:down 1:stay 2:up
    if (CurrentVolume == 5) {
      // Low Spectre: stay or up (1, 2)
      FakeDiceDirection = random(1, 3);
    } else if (CurrentVolume == 25) {
      // High Spectre: stay or down
      FakeDiceDirection = random(0, 2);
    } else {
      // Middle Ground: down, stay or up (0, 1, 2)
      FakeDiceDirection = random(0, 4);
    }

    if (FakeDiceDirection == 0) {
      CurrentVolume = CurrentVolume - FakeDiceStep;
      SatellitePlayer.setVolume(CurrentVolume);
    } else if (FakeDiceDirection == 2) {
      CurrentVolume = CurrentVolume + FakeDiceStep;
      SatellitePlayer.setVolume(CurrentVolume);      
    }
    // (If the FakeDiceDirection equals to 1, Volume stays at the previous level.)

    // Reset the timer
    timer = millis();
  }
}
