int trig = 5; //In this section we are defining what the pins on the arduino are being used for
int echo = 6;
int trig2 = 9;
int echo2 = 10;

int ledPin = 13;

bool lightStatus = false; //Here we are defining variables that will be needed later on 
double theTime;
double distance;
double theTime2;
double distance2;

void setup() {
  // put your setup code here, to run once:
  pinMode(trig, OUTPUT); //Defining how I want to use the pins on the arduino (either input or output)
  pinMode(echo, INPUT);
  pinMode(trig2, OUTPUT); 
  pinMode(echo2, INPUT);
  pinMode(ledPin, OUTPUT); 
  Serial.begin(9600); //Initializing the rate at which I'll communicate with my computer
}

void loop() { //The code in this section will run over and over again

  //First Sensor
  digitalWrite(trig, LOW); //Setting the trigger pin to not send anything. Note: For explanation of how the science works, see report.
  delayMicroseconds(2); //Wait

  digitalWrite(trig, HIGH); //Send waves form the trig pin
  delayMicroseconds(10); //It does this for 10 microseconds
  digitalWrite(trig, LOW); //We turn it off again

  theTime = pulseIn(echo, HIGH); //Gathering the amount of time from the echo pin
  distance = theTime*0.0343/2; //Calculating distance

  //Second Sensor
  digitalWrite(trig2, LOW); //Same as first sensor, but using the second sensor instead
  delayMicroseconds(2);

  digitalWrite(trig2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig2, LOW);

  theTime2 = pulseIn(echo2, HIGH);
  distance2 = theTime2*0.0343/2;
  
  //Printing
  Serial.println(distance); //Printing the two distances
  Serial.println(distance2);

  if (Serial.available() == 1) { //Code in this section will only run when I've sent information from my python program
    if (lightStatus == false) { //If the light is turned off, code in this if will run
      digitalWrite(ledPin, HIGH); //Turning the led on
      lightStatus = true; //Keeping track of whether the light is on or off. 
    }
    else{ // If the light is turned on, this will run
      digitalWrite(ledPin, LOW); //Turning led off
      lightStatus = false; //Keeping track of whether light is on or off. In essence, we should flip between this section and the section above each time since the lgiht status changes, thus creating blinking.
    }
  }
  else if (Serial.available() == 2) { //Code will only run once there are two values sent from my python program
    digitalWrite(ledPin, LOW); //Turning light off
    lightStatus = false; //Storing the light status
    Serial.read(); //Clearing the information in the serial by reading the two values
    Serial.read();
  }
  
  delay(1000); //Waits 1 second before going back to the top of the loop and running again

}
