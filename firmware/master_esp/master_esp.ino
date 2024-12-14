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

#define ECHO 22
#define TRIG 23

#define servoHorizontalPin 18
#define servoVerticalPin 19

#define HORIZ_MIN ((int)45)
#define HORIZ_MAX ((int)135)
#define VERTIC_MIN ((int)45)
#define VERTIC_MAX ((int)135)

uint8_t pwm_req;
String request;

const char* ssid = "ESP_safesight";
const char* password = "ESP_safesight";

IPAddress local_IP(192, 168, 4, 1);  
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 255, 0);

WiFiServer server(10000);
WiFiClient client;

Servo servoHorizontal;
Servo servoVertical;

volatile int duration;

// function declaration //
String removeWhitespaces(String);
String receive_req(void);

void servo_scan();
int distance_scan();

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

  // Distance sensor
  pinMode(TRIG, OUTPUT);
  digitalWrite(TRIG, LOW);
  pinMode(ECHO, INPUT);

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
        else if (request == "scandistance") 
        {
          servo_scan();
        }
        else 
        {
          client.println("wrong command");
        }
      }
    }
  }
}




// User code begin
String receive_req()
{
  String req = client.readStringUntil('\r');
  req = removeWhitespaces(req);

  return req;
}

String removeWhitespaces(String str) 
{
  String result = "";
  for (unsigned int i = 0; i < str.length(); i++) {
    if (!isWhitespace(str[i])) {
      result += str[i];
    }
  }
  return result;
}

void servo_scan() 
{
  servoHorizontal.write(45);
  servoVertical.write(45);

  int flag = 1;
  for (int i = HORIZ_MIN; i <= HORIZ_MAX; i+=2) {
    servoHorizontal.write(i);

    Serial.print("horiz: ");
    Serial.println(i);

    delay(30);
    if (flag == 1) {
      for (int j = VERTIC_MIN; j <= VERTIC_MAX; j+=2) {
        servoVertical.write(j);

        duration = distance_scan();
        client.print(duration);
        client.print(',');

        Serial.print(duration);
        Serial.print(',');

        delay(50);
      }
    } else {
      for (int j = VERTIC_MAX; j >= VERTIC_MIN; j-=2) {
        servoVertical.write(j);
        
        duration = distance_scan();
        client.print(duration);
        client.print(',');

        Serial.print(duration);
        Serial.print(',');

        delay(50);
      }
    }
    flag *= -1;
  }
  client.print('\n');
}

int distance_scan() {
  digitalWrite(TRIG, HIGH);       
  delayMicroseconds(10);

  digitalWrite(TRIG, LOW);       
  int result = pulseIn(ECHO, HIGH);

  if (result > 38000) result = 38000;
   
  return result;
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