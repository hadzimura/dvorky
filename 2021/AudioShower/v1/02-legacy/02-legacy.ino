/*
 * Copyright: DFRobot
 * name:  DFPlayer_Mini_Mp3 sample code
 * Author:  lisper 
 * Date:  2014-05-30
 * Description: sample code for DFPlayer Mini, this code is test on Uno
 *   note: mp3 file must put into mp3 folder in your tf card
 */

#include <SoftwareSerial.h>
#include <dfplayer_mini_mp3.h>

void setup () {
 Serial.begin (9600);
 mp3_set_serial (Serial); //set Serial for DFPlayer-mini mp3 module 
 mp3_set_volume (10);
}

void loop () {        

 mp3_play (1); //play 0001.mp3
 delay (10000); //10 sec, time delay to allow 0001.mp3 to finish playing

 mp3_play (2);
 delay (5000);

 mp3_play (5);
 delay (5000);

 mp3_play (20); //play 0020.mp3
 delay (9000);

 mp3_play (81);
 delay (6000);

 mp3_play (74); //play 0074 mp3
 delay (6000);

}
