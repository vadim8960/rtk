int left_motors_dir = 5;
int left_motors_pwr = 6;
int right_motors_dir = 10;
int right_motors_pwr = 11;

#include <Servo.h>

Servo servo;

const int count_value = 6;

int data[count_value] = {};

void parseData(String input) {
  String tmp = "";
  for (int iter = 0, j = 0; iter < input.length() && j < count_value; ++iter) {
    if (input[iter] == '.' || input[iter] == ' ') {
      while (input[iter] != ' ') iter++;
      data[j] = tmp.toInt();
      tmp = ""; ++j;
    } else {
      tmp += input[iter];
    }
  }
}

void normalizingData() {
  for (unsigned iter = 0; iter < 2; ++iter)
    if (100 < data[iter] && data[iter] < 154)
      data[iter] = 127;
}

void setup() {
  Serial.begin(115200);
  pinMode(left_motors_dir, OUTPUT);
  pinMode(left_motors_pwr, OUTPUT);
  pinMode(right_motors_dir, OUTPUT);
  pinMode(right_motors_pwr, OUTPUT);

  pinMode(13, OUTPUT);

  servo.attach(9);
  servo.write(0);

  while (true) {
    if (Serial.available() > 0) {
      String input_data = Serial.readStringUntil('\n');
      parseData(input_data);
      normalizingData();
    }
    if (data[0] == 127 && data[1] == 127 && data[2] == 0 && data[3] == 0 && data[4] == 0) 
      break;
  }
  
}

void loop() {
  if (Serial.available() > 0) {
    String input_data = Serial.readStringUntil('\n');
    parseData(input_data);
    normalizingData();
  }
  if (data[2]) {
    servo.write(data[5]);
    data[5] -= 127;
    digitalWrite(13, HIGH);
//    if(50-data[5]>0)
//    {
//      digitalWrite(left_motors_dir, 0);
//      analogWrite(left_motors_pwr, constrain(50 - data[5], 0, 200));    
//    }
//    else
//    {
//      digitalWrite(left_motors_dir, 1);
//      //analogWrite(left_motors_pwr, 0);
//      analogWrite(left_motors_pwr, constrain(abs(50 - data[5]), 0, 200));
//    }
//    if((50-data[5]>0))
//    {
//      digitalWrite(right_motors_dir, 0);
//      analogWrite(right_motors_pwr,constrain(50 + data[5], 0, 200));    
//    }
//    else
//    {
//      digitalWrite(right_motors_dir, 1);
//      //analogWrite(right_motors_pwr,abs(0));
//      analogWrite(right_motors_pwr, constrain(abs(50 + data[5]), 0, 200));
//    }

    
    digitalWrite(left_motors_dir, 0);
    digitalWrite(right_motors_dir, 0);
    analogWrite(left_motors_pwr, constrain(75 + data[5], 0, 200));
    analogWrite(right_motors_pwr,constrain(75 - data[5], 0, 200)); 
    
    delay(100);
  } 
  
  if(!data[2]) {
    digitalWrite(13, LOW);
    int fb_power = data[4] - data[3];             // forward backward power
    int rl_power = map(data[0], 0, 255, -255, 255); // right left power

    digitalWrite(left_motors_dir, !(fb_power + rl_power > 0));
    digitalWrite(right_motors_dir, !(fb_power - rl_power > 0));
    
    analogWrite(left_motors_pwr, constrain(abs(fb_power + rl_power), 0, 255));
    analogWrite(right_motors_pwr, constrain(abs(fb_power - rl_power), 0, 255));
  }
}
