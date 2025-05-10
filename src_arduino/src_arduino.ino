#include <TimerOne.h>

int Apin = 2;
int Bpin = 3;
int LEDpin = 4;
volatile bool Aprev = 0;
volatile bool Bprev = 0;
int distancePrinted = 0;
volatile int distance = 0;
volatile bool distanceChanged = false;
bool madePhoto = false;

void setup() {

  Serial.begin(9600);

  pinMode(Apin, INPUT_PULLUP);
  pinMode(Bpin, INPUT_PULLUP);
  pinMode(LEDpin, OUTPUT);
  digitalWrite(LEDpin, HIGH);
  
  attachInterrupt(digitalPinToInterrupt(Apin), pinChangeInterrupt, CHANGE); // задаем обработчик прерываний
  attachInterrupt(digitalPinToInterrupt(Bpin), pinChangeInterrupt, CHANGE); // задаем обработчик прерываний
}

void loop() {
  Serial.println(distance);

  if (distance < distancePrinted){
    if (!madePhoto) {
      Serial.println('P');
      madePhoto = true;
    }
  }
  else if (distance > distancePrinted){
    madePhoto = false;
  }

  noInterrupts();
  distanceChanged = false;
  distancePrinted = distance;
  interrupts();

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
