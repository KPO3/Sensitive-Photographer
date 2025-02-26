#include <TimerOne.h>

int Apin = 2;
int Bpin = 3;
volatile bool Aprev = 0;
volatile bool Bprev = 0;
int distancePrinted = 0;
volatile int distance = 0;
volatile bool distanceChanged = false;
int flatLen = 1;
bool flatCountingIsUp = false;
bool flatEstablished = false;
int flatCounter = 0;
int maxDistance = -1000;
bool maxEstablished = false;
int setUpCounter = 0;
int setUpTime = 100;

void setup() {

  Serial.begin(9600);

  pinMode(Apin, INPUT_PULLUP);
  pinMode(Bpin, INPUT_PULLUP);

  
  attachInterrupt(digitalPinToInterrupt(Apin), pinChangeInterrupt, CHANGE); // задаем обработчик прерываний
  attachInterrupt(digitalPinToInterrupt(Bpin), pinChangeInterrupt, CHANGE); // задаем обработчик прерываний
}

void loop() {
  Serial.println(distance);
  if (!maxEstablished){
    if (setUpCounter < setUpTime){
      setUpCounter++;
      if (distance >= maxDistance){
        maxDistance = distance;
      }
    } else {
        setUpCounter = 0;
        maxEstablished = true;
        Serial.print("Max Established:");
        Serial.println(maxDistance);
    }
  }
  else if (!flatEstablished){
    if (flatCountingIsUp && distancePrinted == distance) {
      if (distance == maxDistance){
        flatLen++;
      }
      else {
        flatEstablished = true;
        Serial.print("Flat length Established:");
        Serial.println(flatLen);
      }
    }
    else {
      if (distancePrinted != distance) {
        flatCountingIsUp = true;
      }
    }
  }

  noInterrupts();
  distanceChanged = false;
  distancePrinted = distance;
  interrupts();

  if (distance == maxDistance){
    flatCounter++;
    if (flatCounter == flatLen / 2){
      Serial.println('P');
    }
  }
  else {
    flatCounter = 0;
  }
  delay(100);
}
void pinChangeInterrupt(){
  bool A = digitalRead(Apin);
  bool B = digitalRead(Bpin);
  
  if (Aprev == B) {
    distance--;
  }
  else {
    distance++;
  }
  distanceChanged = true;
  
  Aprev = A;
  Bprev = B;
}