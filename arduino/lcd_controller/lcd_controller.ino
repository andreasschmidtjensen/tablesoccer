#include <LiquidCrystal.h>
#include "pitches.h"

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);  // init cols and rows
  lcd.print("init");
}

void loop() {
  if (Serial.available()) {
    delay(100);

    // first char declares what we receive
    char c = Serial.read();
    if (c == 'S') { // SOUND
      c = Serial.read();
      
      int t = NOTE_A5; // DEFAULT (HOME)
      if (c == 'A') t = NOTE_C5; // AWAY
      
      tone(2, t, 500); 
    } else if (c == 'D') { // DISPLAY
      lcd.clear();
      while (Serial.available() > 0) {
        c = Serial.read();
        if (c == '\n') {
          lcd.setCursor(0, 1); // first col, second line
        } else {
          lcd.write(c);
        }
      }
    }   
  }
}
