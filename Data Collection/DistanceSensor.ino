const int trigPin = 8; 
const int echoPin = 9; 
const int MAX_DISTANCE =300;
long frontDuration;
int frontDistanceCm;
int d=0;
void setup() {
Serial.begin(2400);
pinMode(trigPin, OUTPUT);
pinMode(echoPin, INPUT);
}

int calDisFront(){
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
digitalWrite(trigPin, HIGH);
delayMicroseconds(15);
digitalWrite(trigPin, LOW);
frontDuration = pulseIn(echoPin, HIGH);
frontDistanceCm= frontDuration*0.034/2;
if(frontDistanceCm>MAX_DISTANCE){
  frontDistanceCm=MAX_DISTANCE;}
  return (frontDistanceCm);
}
void loop() {
  // put your main code here, to run repeatedly:
d=calDisFront();
Serial.println(d);
delay(200);
}
