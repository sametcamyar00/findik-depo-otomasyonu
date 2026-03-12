#include <Arduino.h>
#include "DHTesp.h"
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <PubSubClient.h>

const int DHT_PIN = 15;
const int RELAY_PIN = 4;

DHTesp dht;
LiquidCrystal_I2C lcd(0x27, 16, 2); 

// Wi-Fi ve MQTT Ayarları (Wokwi'nin sanal ağı)
const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.hivemq.com"; // Ücretsiz, genel test sunucusu
const char* mqtt_topic = "samet_findik_depo_2026"; // Python ile bu adresi dinleyeceğiz

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  lcd.clear();
  lcd.print("WiFi Baglaniyor...");
  WiFi.begin(ssid, password, 6); // Wokwi için kanal 6 optimizasyonu
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  lcd.clear();
  lcd.print("WiFi Baglandi!");
  delay(1000);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32_Findik_Client")) {
      // Başarıyla bağlandı
    } else {
      delay(5000);
    }
  }
}

void setup() {
  lcd.init();
  lcd.backlight();
  
  dht.setup(DHT_PIN, DHTesp::DHT22);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  TempAndHumidity data = dht.getTempAndHumidity();

  if (isnan(data.temperature) || isnan(data.humidity)) {
    return;
  }

  // LCD Ekran Güncellemesi
  lcd.setCursor(0,0);
  lcd.print("S:");
  lcd.print(data.temperature, 1);
  lcd.print("C N:%");
  lcd.print(data.humidity, 1);

  int fanDurumu = 0;
  lcd.setCursor(0,1);
  if(data.humidity > 65.0) {
    digitalWrite(RELAY_PIN, HIGH);
    lcd.print("FAN: ACIK (RISK)");
    fanDurumu = 1; // 1: Açık
  } else {
    digitalWrite(RELAY_PIN, LOW);
    lcd.print("FAN: KAPALI     ");
    fanDurumu = 0; // 0: Kapalı
  }
  
  // Python'a Gönderilecek Veri Paketi (Format: Sicaklik,Nem,FanDurumu)
  char payload[50];
  snprintf(payload, sizeof(payload), "%.1f,%.1f,%d", data.temperature, data.humidity, fanDurumu);
  
  // Veriyi MQTT Sunucusuna fırlat
  client.publish(mqtt_topic, payload);
  
  delay(2000); 
}