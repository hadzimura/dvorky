#include <SPI.h>
#include <SD.h>
#include <Arduino.h>

#define CS_PIN 10

//#define DELETE_FILE

File myFile;
const char* fileName = "test.txt";

bool isFileExist(const char* fileName){
  //kontrola, zda soubor existuje 
  if(SD.exists(fileName)){
    //soubor existuje
    Serial.print("Soubor "); Serial.print(fileName); Serial.println(" nalezen.\n");
    return true;
  }
  else{
    //soubor neextistuje
    Serial.print("Soubor "); Serial.print(fileName); Serial.println(" neexistuje.\n");

    //vytvoření souboru
    myFile = SD.open(fileName, FILE_WRITE);
    myFile.flush();
    myFile.close();
    
    Serial.print("Soubor "); Serial.print(fileName); Serial.println(" vytvořen.\n");
    return false;
  }
}

void writeToFile(const char* fileName, uint8_t number){
  //zápis do souboru
  //otevření souboru pro zápis
  myFile = SD.open(fileName, FILE_WRITE);

  Serial.print("Zapisuji do souboru: "); Serial.println(fileName);
  Serial.print("Cislo: "); Serial.println(number);
  myFile.print("Cislo: "); myFile.println(number);
  //čekej než je zápis dokončen
  myFile.flush();

  //uzavři soubor
  myFile.close();
  Serial.println("Zapis dokoncen a soubor uzavren.\n");
}

void readFile(const char* fileName){
  //čtení souboru
  //otevření souboru pro čtení
  myFile = SD.open(fileName, FILE_READ);
  Serial.print("Cteni ze souboru: "); Serial.println(fileName);
  Serial.print("Obsah souboru: \n");

  //čti
  while (myFile.available()) {
    Serial.write(myFile.read());
  }

  //uzavři soubor
  myFile.close();
  Serial.println("Cteni dokonceno a soubor uzavren.\n");
}

void deleteFile(const char* fileName){
  SD.remove(fileName);
  Serial.println("Soubor smazan. \n");
}

void setup() {
  Serial.begin(9600);
  delay(1);

  Serial.println("(Serial Port Ready)");
  Serial.println("SD Init...");
  if (!SD.begin(CS_PIN)) {
    Serial.println("SD karta neni vlozena!");
    while (1);
  }
  Serial.println("Sd karta pripravena.");
}

void loop() {
  if(isFileExist(fileName)){
    //zapiš nahodné čislo od 0 do 255
    writeToFile(fileName, random(0, 255));
    delay(2000);
    //přečti zapsané číslo
    readFile(fileName);
    delay(2000);
    #ifdef DELETE_FILE
      //smaž soubor
      deleteFile(fileName);
    #endif
    delay(5000);
  }
  delay(2000);
}
