#include <Arduino.h>
#include <WiFi.h>

#include <ESP32Servo.h>

#define LED 2

#define IN1 33
#define IN2 25
#define IN3 32
#define IN4 26

#define ENA 17
#define ENB 16

#define servoHorizontalPin 18
#define servoVerticalPin 19

uint8_t pwm_req;
String request;

const char* ssid = "ESP_safesight";
const char* password = "ESP_safesight";

IPAddress local_IP(192, 168, 1, 1);  
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

WiFiServer server(10000);
WiFiClient client;


Servo servoHorizontal;
Servo servoVertical;

// function declaration //
String removeWhitespaces(String);
String receive_req(void);

void servo_scan();

void motor_A_forw(void);
void motor_B_forw(void);
void motor_A_back(void);
void motor_B_back(void);

void move_forw(void);
void move_back(void);
void move_right(void);
void move_left(void);
void move_stop(void);



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);

  // motor control outputs
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // PWM motor speed outputs
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Servo setup
  servoHorizontal.attach(servoHorizontalPin); 
  servoVertical.attach(servoVerticalPin); 
  servoHorizontal.write(45);
  servoVertical.write(45);

  // wifi setup
  if (!WiFi.softAPConfig(local_IP, gateway, subnet)) {
    Serial.println("Failed to configure static IP for AP");
  }

  WiFi.softAP(ssid, password);
  Serial.println("Access Point started");

  server.begin();
  Serial.println("Server started");

  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());
}

void loop() {
  servo_scan();

  /*
  client = server.available();
  if (client)
  {
    while (client.connected())
    {
      if (client.available()) 
      { 
        request = receive_req();

        if (request == "forward")
        {
          move_forw();
        }
        else if (request == "backward") 
        {
          move_back();
        }
        else if (request == "right") 
        {
          move_right();
        }
        else if (request == "left") 
        {
          move_left();
        }
        else if (request == "stop") 
        {
          move_stop();
        }
        else 
        {
          client.println("wrong command");
        }
      }
    }
  }
  */
}




// User code begin
String receive_req()
{
  String req = client.readStringUntil('\r');
  req = removeWhitespaces(req);

  return req;
}

String removeWhitespaces(String str) {
  String result = "";
  for (unsigned int i = 0; i < str.length(); i++) {
    if (!isWhitespace(str[i])) {
      result += str[i];
    }
  }
  return result;
}

void servo_scan() {
  int flag = 1;
  for (int i = 45; i <= 135; i+=2) {
    servoHorizontal.write(i);
    delay(15);
    if (flag == 1) {
      for (int i = 45; i <= 135; i+=2) {
        servoVertical.write(i);
        //measurement and transmit
        delay(30);
      }
    } else {
      for (int i = 135; i >= 45; i-=2) {
        servoVertical.write(i);
        //measurement and transmit
        delay(30);
      }
    }
    flag *= -1;
  }
  //send end of transmission
}

void motor_A_forw(){
  digitalWrite(ENA, HIGH);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
}

void motor_B_forw(){
  digitalWrite(ENA, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void motor_A_back(){
  digitalWrite(ENB, HIGH);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
}

void motor_B_back(){
  digitalWrite(ENB, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void motor_A_stop(){
  digitalWrite(ENB, LOW);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}

void motor_B_stop(){
  digitalWrite(ENB, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}


void move_forw()
{
  motor_A_forw();
  motor_B_forw();
}

void move_back()
{
  motor_A_back();
  motor_B_back();
}

void move_right()
{
  motor_A_forw();
  motor_B_back();
}

void move_left()
{
  motor_A_back();
  motor_B_forw();
}

void move_stop()
{
  motor_A_stop();
  motor_B_stop();
}
// User code end