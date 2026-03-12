# 🌰 Akıllı Fındık Deposu İklimlendirme ve Havalandırma Sistemi

Bu proje, fındık hasadı sonrasında kurutma ve depolama süreçlerinde karşılaşılan küflenme (aflatoksin) problemini önlemek amacıyla geliştirilmiş, uçtan uca bir **IoT (Nesnelerin İnterneti)** çözümüdür. 

Gömülü sistemler ve veri görselleştirme teknolojileri kullanılarak, deponun mikro-kliması anlık olarak izlenir ve riskli durumlarda havalandırma sistemleri otonom olarak devreye girer.

## 🚀 Projenin Özellikleri

* **Gerçek Zamanlı İzleme:** Ortam sıcaklığı ve bağıl nem oranının DHT22 sensörü ile hassas ölçümü.
* **Otonom Karar Mekanizması:** Nem oranı %65'i aştığında mikrodenetleyici (ESP32) üzerinden rölenin tetiklenmesi ve havalandırma fanının otomatik çalıştırılması.
* **Yerel Görüntüleme:** I2C LCD ekran üzerinden depo başındaki operatörler için anlık durum gösterimi.
* **Bulut Haberleşmesi (IoT):** Verilerin endüstri standardı olan **MQTT protokolü** kullanılarak kablosuz ağ üzerinden sunucuya aktarılması.
* **Canlı Kontrol Paneli (Dashboard):** Python ve Matplotlib kullanılarak geliştirilen, çift eksenli (Dual-Axis) ve anlık güncellenen profesyonel veri izleme arayüzü.

## 🛠️ Kullanılan Teknolojiler

**Donanım ve Gömülü Sistem:**
* **Platform:** Wokwi Simülatörü & PlatformIO (VS Code)
* **Mikrodenetleyici:** ESP32 DevKit
* **Diller / Çatılar:** C/C++, Arduino Framework
* **Bileşenler:** DHT22 Sensörü, 5V Röle Modülü, 16x2 I2C LCD Ekran

**Yazılım ve Arayüz:**
* **Dil:** Python 3
* **Kütüphaneler:** `paho-mqtt` (Haberleşme), `matplotlib` (Veri Görselleştirme)
* **Sunucu:** HiveMQ Public Broker

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

### 1. Gömülü Sistem (ESP32) Tarafı
1. VS Code üzerinden **PlatformIO** eklentisini kurun.
2. Bu repository'yi bilgisayarınıza indirin (Clone).
3. VS Code'da projeyi açın ve alt kısımdaki `Build` (✓) butonuna basarak kütüphaneleri yükleyip C kodunu derleyin.
4. **Wokwi Simulator** eklentisi ile `diagram.json` dosyası üzerinden simülasyonu başlatın. (Sistem otomatik olarak Wokwi-GUEST ağına ve MQTT sunucusuna bağlanacaktır.)

### 2. Arayüz (Python) Tarafı
1. Bilgisayarınızda Python yüklü olduğundan emin olun.
2. Gerekli kütüphaneleri kurmak için terminale şu komutu girin:
   ```bash
   pip install paho-mqtt matplotlib
