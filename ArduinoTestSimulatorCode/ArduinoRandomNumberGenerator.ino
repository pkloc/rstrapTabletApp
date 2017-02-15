long randNumber;
long randNumber2;

void setup(){
  Serial.begin(9600);

  // if analog input pin 0 is unconnected, random analog
  // noise will cause the call to randomSeed() to generate
  // different seed numbers each time the sketch runs.
  // randomSeed() will then shuffle the random function.
  randomSeed(analogRead(0));
}

void loop() {
  
  randNumber = random(250, 300);
  randNumber2 = random(10, 20);

  String output = String(randNumber);
  output += ',';
  output += randNumber2;
  
  Serial.println(output);
  
  delay(1000);
}


