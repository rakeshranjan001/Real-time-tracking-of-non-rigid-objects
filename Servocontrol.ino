String Input;
#include <Servo.h> 

Servo servo1;  // Create a Servo object for each servo

// Initialize the variables used 

int pos;
int pos_map;

// the setup function runs once when you press reset or power the board

void setup() 
{
  servo1.attach(9);  //Servo is attached to Pin 9
  Serial.begin(9600);
}

// the loop function runs over and over again forever

void loop() 
{
   if (Serial.available() > 0) 
   {
        Input = Serial.read();   // Read the first byte
   }
   pos=Input.toInt();       //Converting the string data to its corresponding integer value
   pos=pos*3;
   Serial.println(pos);   
   pos_map=map(pos,0,640,0,180); // Mapping the received data from 0 to 180
   Serial.println(pos_map);
   servo1.write(pos_map);   // Moving the servo to received data
}
