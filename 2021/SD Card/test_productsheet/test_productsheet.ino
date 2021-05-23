#define SERIAL_BAUDRATE 9600
#define CS_PIN 4
#include <SPI.h>
#include <SD.h>

File myFile;
int counter = 0;
void setup() {
  // initialize serial communication
  Serial.begin(SERIAL_BAUDRATE);
  delay(1);
  Serial.print("Initializing SD card...");
  if (!SD.begin(CS_PIN)) {
    Serial.println("initialization failed!");
    while (1);
  }
  Serial.println("initialization done.");
}
void loop() {
  counter++;
  myFile = SD.open("test.txt", FILE_WRITE);
  // if the file opened okay, write to it:
  if (myFile) {
    Serial.println("Zapisuji do souboru...");
    myFile.print(counter);
    myFile.println(". zapis;");
    Serial.print(counter);
    Serial.println(". zapis");
    // close the file:
    myFile.close();
    Serial.println("Hotovo");
  } else {
    // if the file didn't open, print an error:
    Serial.println("Chyba pri otevirani souboru");
  }
  // re-open the file for reading:
  myFile = SD.open("test.txt");
  if (myFile) {
    Serial.println("***************");
    Serial.println("Obsah souboru: ");
    // read from the file until there's nothing else in it:
    while (myFile.available()) {
      Serial.write(myFile.read());
    }
    Serial.println("***************");
    // close the file:
    myFile.close();
  } else {
    // if the file didn't open, print an error:
    Serial.println("Chyba pri otevirani souboru");
  }
  delay(3000);
}
