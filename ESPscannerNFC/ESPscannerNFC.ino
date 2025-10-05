#include <SPI.h>
#include <MFRC522.h>

const uint8_t SCK_PIN  = 6;
const uint8_t MISO_PIN = 4;
const uint8_t MOSI_PIN = 5;
const uint8_t SS_PIN   = 10;
const uint8_t RST_PIN  = 9;
const uint8_t BUZZER_PIN = 3;

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  pinMode(BUZZER_PIN, OUTPUT);
  while (!Serial) { delay(10); }
  SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, SS_PIN);
  rfid.PCD_Init();
  Serial.println("RC522 ready. Scan a tag...");
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  tone(BUZZER_PIN, 1000); // Valid beep
  delay(100);
  noTone(BUZZER_PIN);


  // Print UID as HEX string (no spaces)
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) Serial.print("0");
    Serial.print(rfid.uid.uidByte[i], HEX);
  }
  Serial.println();

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
  delay(300);

  while (!Serial.available());
  int x = Serial.readString().toInt();
  
  if(x == 1) {
    
} else {
    tone(BUZZER_PIN, 100); // Invalid beep
    delay(1000);
}
noTone(BUZZER_PIN);
}
