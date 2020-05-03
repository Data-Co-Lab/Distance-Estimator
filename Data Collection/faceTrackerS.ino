#include <Servo.h>

Servo myservoX;  // create servo object to control a servo
Servo myservoY;
// twelve servo objects can be created on most boards

byte buf[2];
int dcx = 165;  //[100,180]
int dcy =90;  //[70,130] inversed
boolean data=false;
byte x=0;
void setup() {
  Serial.begin(9600);
  myservoX.attach(6);  // attaches the servo on pin 9 to the servo object
  myservoY.attach(9);
  myservoX.write(dcx);
  myservoY.write(dcy);
  
    x=Serial.read();
    while(x!= 42){
      //data=false;
      x=Serial.read();
      //Serial.println(x);
      delay(1);
    }
  delay(100);
  data=true;
}

void loop() {
  while(data==true){
       readData();
       servos();
       delay(10);
        }
}
void servos(){
  //if (buf[0]>0 && buf[1]>0){
    myservoX.write(dcx);
    myservoY.write(dcy);
    dcx=buf[0];
    dcy=buf[1];
    /*Serial.print("x: ");
    Serial.print(dcx);
    Serial.print('\t');
    Serial.print("y: ");
    Serial.println(dcy);
    delay(10);*/
    dcx=constrain(dcx,100,180);
    dcy=constrain(dcy,70,130);

  /*Serial.print("x: ");
  Serial.print(dcx);
  Serial.print('\t');
  Serial.print("y: ");
  Serial.println(dcy);
  delay(100);*/
  //}
}
void readData(){
if (Serial.available() >=2) {
        buf[0]=Serial.read();
        buf[1]=Serial.read();
        }
}
