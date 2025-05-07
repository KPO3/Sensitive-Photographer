#include <TimerOne.h>

int Apin = 2;
int Bpin = 3;
volatile bool Aprev = 0;
volatile bool Bprev = 0;
int distancePrinted = 0;
volatile int distance = 0;
volatile bool distanceChanged = false;
int flatLen = 0;
bool flatCountingEnabled = false;
bool flatEstablished = false;
int flatCounter = 1;
int maxDistance = -1000;
bool maxEstablished = false;
int setUpCounter = 0;
int setUpTime = 100;
long lastPhoto = 0;
long span = 3;
long period = 5;

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
  else if (!flatEstablished) {
    if (flatCountingEnabled) { //Считаем только при включенном счете
      if (distance == maxDistance) { // Если текущее значение максимум - считаем
          flatLen++;
      }
      else if (distancePrinted == maxDistance) { // Если предыдущее значение было максимумом, а текущее - нет, то фиксируем максимум
        flatEstablished = true;
        Serial.print("Flat length Established:");
        Serial.println(flatLen);
      }
    }
    else if (distance != maxDistance) { // Счет включается только когда мы не находимся на верхней полке (максимуме)
      flatCountingEnabled = true;
    }
  }
  //unsigned long time = millis();
  //Serial.print("TEST: "); Serial.print(time); Serial.print(" - "); Serial.print(lastPhoto); Serial.print(" - "); Serial.println(period); 
  if (distance == distancePrinted && flatEstablished ){ //&& time >= lastPhoto + period - span
    flatCounter++;
    if (flatCounter == flatLen / 2){
      Serial.println('P');
      //if (lastPhoto != 0) period = time - lastPhoto;
      //lastPhoto = time;
    }
  noInterrupts();
  distanceChanged = false;
  distancePrinted = distance;
  interrupts();
  }
  else {
    flatCounter = 1;
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