// uses a library https://github.com/yoursunny/esp32cam
#include <esp32cam.h>
#include <WebServer.h>
#include <WiFi.h>

static const int  PIN_FLASH = 4;

static const char* WIFI_SSID = "ESP_safesight";
static const char* WIFI_PASS = "ESP_safesight";

WebServer server(80);

void capture() {
  auto img = esp32cam::capture();
  if(img == nullptr){
    server.send(500, "", "");
    return;
  }
  server.setContentLength(img->size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  img->writeTo(client);
}

void flash_on(){
  digitalWrite(PIN_FLASH, 1);
}

void flash_off(){
  digitalWrite(PIN_FLASH, 0);
}

void setup() {
  pinMode(PIN_FLASH, OUTPUT);
  digitalWrite(PIN_FLASH, 0);
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("wifi error");
    ESP.restart();
  }
  Serial.println("wifi ok");

  {
    using namespace esp32cam;

    auto res = Resolution::find(640, 480);

    esp32cam::Config cfg;
    cfg.setPins(esp32cam::pins::AiThinker);
    cfg.setResolution(res);
    cfg.setJpeg(40);

    bool ok = Camera.begin(cfg);
    if (!ok) {
      Serial.println("camera error");
      ESP.restart();
    }
    Serial.println("camera ok");
  }

  Serial.println(WiFi.localIP());

  server.on("/image", capture);
  server.on("/flashon", flash_on);
  server.on("/flashoff", flash_off);
  server.begin();
}

void loop() {
  server.handleClient();
}