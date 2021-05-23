// Chebske Dvorky 2021
// ASP (Arduino Satellite Player)

#include <SD.h>     // Arduino SD Card 
#include <TMRpcm.h> // Arduino asynchronous playback of PCM/WAV
#include <SPI.h>    // Arduino SPI

TMRpcm audio;       // Arduino TRMpcm audio object initialization

// PINOUT
const unsigned int SD_CS_PIN = 4;
const unsigned int MINI_SPEAKER = 31;
const unsigned int ECHO_PIN = 32;
const unsigned int TRIG_PIN = 33;
//const unsigned int SWITCH_PIN = 35;

const unsigned int BAUD_RATE = 9600;

//int temp=1;
//int pp=5;
//int next=6;
//int prev=7;

void setup()
{ 
//  pinMode(pp,INPUT_PULLUP);
//  pinMode(next,INPUT_PULLUP);
//  pinMode(prev,INPUT_PULLUP);

  // SRF05
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
//  pinMode(SWITCH_PIN, INPUT);

  // Serial Console Initialization
  Serial.begin(BAUD_RATE);
  Serial.println("Serial Console Init...");

  // Audio Initialization
  Serial.println("[Audio] Init...");
  audio.speakerPin = 45; //5,6,11 or 46 on Mega, 9 on Uno, Nano, etc
  audio.setVolume(5);

  // SD Card Initialization
  Serial.println("[SD Card] Init...");
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("[SD Card] Initialization Failed!");
    return;
  } else {
    Serial.println("[SD Card] Initialization Succesful");

    // Welcome sound (playback test)
    // This will play each time the ASP powers up, or is reset
    Serial.println("[Audio] Play init chime test...");
 
    if (SD.exists("boot.wav")) {
      Serial.println("[Audio] Boot chime (boot.wav) file found");
      audio.play("boot.wav");
    } else {
      Serial.println("[Audio] Boot chime (boot.wav) file missing!");
    }
  }
}

void loop() {
  
  // HY-SRF05 Ultrasonic Measurement Settings
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  // Measurement Calculation
  const unsigned long duration = pulseIn(ECHO_PIN, HIGH);
  int distance = duration/29/2;
  int sound = duration;

  // Measurement Evaluation
  if(duration==0){
    // Failure to read data from sensor
    Serial.println("[Ultrasonic] Warning, no pulse from sensor!");
  } else{
    // Data from sensor acquired
    Serial.print("[Ultrasonic] duration/cm/Hz: ");
    Serial.print(duration);
    Serial.print(" / ");
    Serial.print(distance);
    Serial.print(" / ");
    Serial.println(sound);
    // Play note
    Serial.println("playing");
    if (distance<10) {
      tone(MINI_SPEAKER, 100, 30);
    } else if (distance>=10 && distance<=30) {
      tone(MINI_SPEAKER, 200, 30);  
    } else if (distance>30 && distance<=50) {
      tone(MINI_SPEAKER, 300, 30);  
    } else {
      tone(MINI_SPEAKER, 400, 30);  
     }

    
  }
//  delay(100);
}
