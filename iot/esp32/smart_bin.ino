// GreenTrace ESP32 starter sketch
// Connect ultrasonic sensor to TRIG/ECHO and replace Wi-Fi/API values.
// The prototype sends fill-level telemetry to FastAPI.

#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* API_URL = "http://YOUR_PC_IP:8000/api/bins/BIN-LAB-03/telemetry";

const int TRIG_PIN = 5;
const int ECHO_PIN = 18;

float distanceCm() {
  digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  return duration * 0.0343 / 2.0;
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void loop() {
  float d = distanceCm();
  float fill = constrain(100.0 - (d / 40.0 * 100.0), 0, 100);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");
    String body = "{\"fill_level\":" + String(fill) + ",\"temperature\":29,\"battery\":92}";
    http.PATCH(body);
    http.end();
  }
  delay(10000);
}