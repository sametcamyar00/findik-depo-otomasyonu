import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker

# --- AYARLAR ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "samet_findik_depo_2026"

zaman_serisi = []
sicaklik_verisi = []
nem_verisi = []
sayac = 0  # Zaman ekseninin sürekli ilerlemesi için

# Modern bir arka plan stili ayarlayalım
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('ggplot')

# Grafik penceresini oluştur (Daha geniş ve ferah)
fig, ax1 = plt.subplots(figsize=(12, 6))
fig.canvas.manager.set_window_title('Akıllı Depo Monitörü')

# İkinci Y Ekseni (Nem için sağ tarafı kullanacağız)
ax2 = ax1.twinx()

# --- MQTT FONKSİYONLARI ---
def baglaninca_ne_yap(client, userdata, flags, rc):
    print("🌍 Bulut Sunucusuna (MQTT) Bağlanıldı! Veriler bekleniyor...")
    client.subscribe(MQTT_TOPIC)

def mesaj_gelince_ne_yap(client, userdata, msg):
    global sayac
    payload = msg.payload.decode("utf-8")
    try:
        sicaklik, nem, fan_durumu = map(float, payload.split(","))
        
        sayac += 2 # Wokwi'de delay(2000) olduğu için 2'şer saniye artırıyoruz
        zaman_serisi.append(sayac)
        sicaklik_verisi.append(sicaklik)
        nem_verisi.append(nem)

        # Ekranda sadece son 20 veriyi göster (Grafik çok sıkışmasın)
        if len(zaman_serisi) > 20:
            zaman_serisi.pop(0)
            sicaklik_verisi.pop(0)
            nem_verisi.pop(0)
            
        fan_mesaji = "⚠️ AÇIK (RİSK!)" if fan_durumu == 1 else "✅ KAPALI"
        print(f"📥 ZAMAN: {sayac}s | Sıcaklık {sicaklik}°C | Nem: %{nem} | Fan: {fan_mesaji}")
    except Exception as e:
        pass

# --- GRAFİK GÜNCELLEME FONKSİYONU ---
def grafigi_guncelle(frame):
    # Eksenleri temizle
    ax1.clear()
    ax2.clear()
    
    # Veri yoksa çizmeyi bekle
    if not zaman_serisi:
        return

    # 1. SICAKLIK ÇİZGİSİ (Sol Eksen - Kırmızı tonları)
    cizgi1 = ax1.plot(zaman_serisi, sicaklik_verisi, label="Sıcaklık (°C)", color="#e63946", linewidth=3, marker='o', markersize=6)
    ax1.set_ylabel("Sıcaklık Değeri (°C)", color="#e63946", fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor="#e63946")
    
    # 2. NEM ÇİZGİSİ (Sağ Eksen - Mavi tonları)
    cizgi2 = ax2.plot(zaman_serisi, nem_verisi, label="Nem Oranı (%)", color="#1d3557", linewidth=3, marker='s', markersize=6)
    ax2.set_ylabel("Bağıl Nem (%)", color="#1d3557", fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor="#1d3557")

    # --- EKSEN VE IZGARA (GRID) AYARLARI ---
    ax1.set_xlabel("Zaman (Saniye)", fontsize=12, fontweight='bold')
    ax1.set_title("Fındık Deposu İklimlendirme ve Havalandırma Monitörü", fontsize=15, fontweight='bold', pad=20)
    
    # X Eksenini sadece tam sayılarla ve belirli aralıklarla böl
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=10))
    
    # Arka plan ızgaralarını estetik hale getir
    ax1.grid(True, which='major', linestyle='--', linewidth=0.7, alpha=0.7)
    ax2.grid(False) # Sağ eksenin gridini kapatıyoruz ki çizgiler birbirine girmesin

    # --- GÖSTERGELER (LEGEND) ---
    cizgiler = cizgi1 + cizgi2
    etiketler = [c.get_label() for c in cizgiler]
    ax1.legend(cizgiler, etiketler, loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=2, frameon=True, shadow=True)

    # Düzeni sıkılaştır (Metinlerin pencere dışına taşmasını engeller)
    fig.tight_layout()

# --- ANA PROGRAM ---
print("🚀 Gelişmiş Arayüz Başlatılıyor...")

istemci = mqtt.Client()
istemci.on_connect = baglaninca_ne_yap
istemci.on_message = mesaj_gelince_ne_yap

istemci.connect(MQTT_BROKER, 1883, 60)
istemci.loop_start() 

ani = animation.FuncAnimation(fig, grafigi_guncelle, interval=2000, cache_frame_data=False)
plt.show()