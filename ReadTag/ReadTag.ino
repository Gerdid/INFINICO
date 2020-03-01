#include <NfcAdapter.h>
#include <PN532/PN532/PN532.h>

#if 0 // use SPI
#include <SPI.h>
#include <PN532/PN532_SPI/PN532_SPI.h>
PN532_SPI pn532spi(SPI, 9);
NfcAdapter nfc = NfcAdapter(pn532spi);
#elif 1 // use hardware serial

#include <PN532/PN532_HSU/PN532_HSU.h>
PN532_HSU pn532hsu(Serial1);
NfcAdapter nfc(pn532hsu);
#elif 0  // use software serial

#include <PN532/PN532_SWHSU/PN532_SWHSU.h>
#include "SoftwareSerial.h"
SoftwareSerial SWSerial(2, 3);
PN532_SWHSU pn532swhsu(SWSerial);
NfcAdapter nfc(pn532swhsu);
#else //use I2C

#include <Wire.h>
#include <PN532/PN532_I2C/PN532_I2C.h>

PN532_I2C pn532_i2c(Wire);
NfcAdapter nfc = NfcAdapter(pn532_i2c);
#endif

void setup(void) {
  Serial.begin(9600);
  Serial.println("NDEF Reader");
  nfc.begin();
  pinMode(13, OUTPUT);
}

int incomingByte = 0;

void loop(void) {
  digitalWrite(13, LOW);
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte == 49) {   //Si se recibe el número 1
      while (1) {
        digitalWrite(13, HIGH);    
        //Serial.println("\nEscanee tarjeta NFC\n");
        if (nfc.tagPresent()) {
          NfcTag tag = nfc.read();
          String UID=tag.getUidString();
          Serial.println(UID);
          break;
        }
      }
    }
  }
}
