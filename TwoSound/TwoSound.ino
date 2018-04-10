int trig = 5;
int echo = 6;
int trig2 = 9;
int echo2 = 10;

int ledPin = 13;
bool lightStatus = false;

double theTime;
double distance;

double theTime2;
double distance2;

//unsigned long start;

void setup() {
  // put your setup code here, to run once:
  pinMode(trig, OUTPUT); 
  pinMode(echo, INPUT);
  pinMode(trig2, OUTPUT); 
  pinMode(echo2, INPUT);
  pinMode(ledPin, OUTPUT); 
  Serial.begin(9600); 
}

void loop() {
  // put your main code here, to run repeatedly:
  
  //First Sensor
  digitalWrite(trig, LOW);
  delayMicroseconds(2);

  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  theTime = pulseIn(echo, HIGH);
  distance = theTime*0.0343*0.394/2;

  //Second Sensor
  digitalWrite(trig2, LOW);
  delayMicroseconds(2);

  digitalWrite(trig2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig2, LOW);

  theTime2 = pulseIn(echo2, HIGH);
  distance2 = theTime2*0.0343*0.394/2;
  
  //Print
  //Serial.print("Sensor 1: ");
  Serial.println(distance);
  //Serial.print("Sensor 2: ");
  Serial.println(distance2);

  if ((Serial.available() > 0) && (Serial.available() < 2)) {
    if (lightStatus == false) {
      digitalWrite(ledPin, HIGH);
      lightStatus = true;
    }
    else{
      digitalWrite(ledPin, LOW);
      lightStatus = false;
    }

    //digitalWrite(ledPin, HIGH);
  }
  else if (Serial.available() == 2) {
    digitalWrite(ledPin, LOW);
    lightStatus = false;
    Serial.read();
    Serial.read();
  }
  
  delay(1000);
  /*unsigned long end = micros();
  unsigned long delta = end - start;
  Serial.println(delta);
  start = micros();*/
}
