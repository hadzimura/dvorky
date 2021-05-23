#include <Wire.h>
#include<RF24.h>

const unsigned int MINI_SPEAKER = 4;
const unsigned int BAUD_RATE = 9600;
const unsigned int CE = 7;
const unsigned int CS = 8;

RF24 radio(CE, CS);
// nastavení adres pro přijímač a vysílač,
// musí být nastaveny stejně v obou programech!
byte adresaPrijimac[]= "prijimac00";
byte adresaVysilac[]= "vysilac00";

void setup() {
  // put your setup code here, to run once:
  RF24 radio(7, 8);
  
  Serial.begin(BAUD_RATE);
  Serial.println("Serial Console Init...");
  
  pinMode(MINI_SPEAKER, OUTPUT); 
  
  // zapnutí komunikace nRF modulu
  radio.begin();
  // nastavení výkonu nRF modulu,
  // možnosti jsou RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH and RF24_PA_MAX,
  // pro HIGH a MAX je nutný externí 3,3V zdroj
  radio.setPALevel(RF24_PA_LOW);
  // nastavení zapisovacího a čtecího kanálu
  radio.openWritingPipe(adresaPrijimac);
  radio.openReadingPipe(1,adresaVysilac);
  // začátek příjmu dat
  radio.startListening();
  tone(MINI_SPEAKER, 200, 200);

}

void loop() {
  // proměnné pro příjem a odezvu
  int prijem;
  unsigned long odezva;
  // v případě, že nRF je připojené a detekuje
  // příchozí data, začni s příjmem dat
  if( radio.available()){
    // čekání na příjem dat
    while (radio.available()) {
      // v případě příjmu dat se provede zápis
      // do proměnné prijem
      radio.read( &prijem, sizeof(prijem) );
    }
  }
  // vytisknutí přijatých dat na sériovou linku
  Serial.print("Prijata volba: ");
  Serial.print(prijem);
  // dekódování přijatých dat
  switch( prijem ) {
    // pro známou hodnotu dat (1,2,3)
    // se odešle odezva:
    case 1:
      // v případě 1 odešli počet milisekund
      // od připojení napájení
      odezva = millis();
      break;
    case 2:
      // v případě 2 počet sekund
      // od připojení napájení
      odezva = millis()/1000;
      break;
    case 3:
      // v případě 3 počet mikrosekund
      // od připojení napájení
      odezva = micros();
      break;
      // v případě ostatních dat bude odezva 0
    default:
      odezva = 0;
      break;
  }
  // ukončení příjmu dat
  radio.stopListening();
  // odeslání odezvy
  radio.write( &odezva, sizeof(odezva) );
  // přepnutí do příjmu dat pro další komunikaci
  radio.startListening();
  // vytištění odezvy po sériové lince
  Serial.println(", odezva: ");
  tone(MINI_SPEAKER, 300, 100);
}
