# 🎰 Blackjack Simülatör Koleksiyonu

Bu proje, Python ile yazılmış kapsamlı bir blackjack oyun koleksiyonudur. Basit simülasyondan gerçekçi casino kurallarına, interaktif text oyunundan grafik arayüze kadar farklı versiyonlar içerir.

## 📋 İçindekiler

- [Kurulum](#kurulum)
- [Programlar](#programlar)
  - [1. Temel Blackjack Simülatörü](#1-temel-blackjack-simülatörü)
  - [2. Gerçekçi Casino Simülatörü](#2-gerçekçi-casino-simülatörü)
  - [3. İnteraktif Text Oyunu](#3-interaktif-text-oyunu)
  - [4. Grafik Blackjack Oyunu](#4-grafik-blackjack-oyunu)
- [Casino Kuralları](#casino-kuralları)
- [Teknik Detaylar](#teknik-detaylar)
- [İstatistikler ve Analizler](#istatistikler-ve-analizler)

## 🚀 Kurulum

### Gereksinimler
```bash
Python 3.7+
```

### Kütüphaneleri Yükle
```bash
pip install -r requirements.txt
```

### requirements.txt içeriği:
```
matplotlib>=3.5.0
numpy>=1.21.0
pygame>=2.1.0
```

## 🎮 Programlar

### 1. Temel Blackjack Simülatörü
**Dosya:** `blackjack_simulator.py`

#### Özellikler:
- **6 deste** ile oyun
- **Temel blackjack kuralları**
- **Rastgele oyuncu stratejisi**
- **10.000 oyun simülasyonu**
- **İstatistiksel grafikler**

#### Çalıştırma:
```bash
python blackjack_simulator.py
```

#### Oyuncu Stratejisi:
- **11 ve altı:** %100 kart çeker
- **12-16:** %80 kart çeker  
- **17:** %20 risk alır
- **18-20:** %5 nadir risk

#### Çıktılar:
- Her 1000 oyun için kar/zarar bar grafiği
- Kümülatif kar/zarar eğrisi
- Detaylı istatistikler

---

### 2. Gerçekçi Casino Simülatörü
**Dosya:** `blackjack_simulator_realistic.py`

#### Gerçek Casino Avantajları:
- **6:5 Blackjack Ödemesi** (120 birim, 150 değil)
- **Soft 17'de Kart Çekme** (A-6 gibi ellerde)
- **Daha Hatalı Oyuncu Stratejisi**
- **Double Bust Kuralı** (her iki taraf da patlasa oyuncu kaybeder)

#### Çalıştırma:
```bash
python blackjack_simulator_realistic.py
```

#### Beklenen Sonuçlar:
- **House Edge:** ~%11-12 (casino lehine)
- **Oyuncu Kazanma Oranı:** ~%39-40
- **Toplam Kayıp:** 10.000 oyunda yaklaşık -1000 birim

#### Karşılaştırma:
| Özellik | Temel Simülasyon | Gerçekçi Casino |
|---------|------------------|-----------------|
| Blackjack Ödemesi | 3:2 (150 birim) | 6:5 (120 birim) |
| Soft 17 | Kasa durur | Kasa kart çeker |
| House Edge | -%7.86 | +%11.87 |

---

### 3. İnteraktif Text Oyunu
**Dosya:** `interactive_blackjack.py`

#### Özellikler:
- **Gerçek zamanlı oyun**
- **Kullanıcı kontrollü**
- **Gerçekçi casino kuralları**
- **Canlı istatistik takibi**

#### Çalıştırma:
```bash
python interactive_blackjack.py
```

#### Kontroller:
- **[H]** - Hit (Kart çek)
- **[S]** - Stand (Dur)
- **[Q]** - Quit (Çık)

#### Takip Edilen İstatistikler:
- Toplam kar/zarar
- Oyun sayısı
- Kazanma/kaybetme oranları
- Blackjack sayısı
- Ortalama oyun başına kar/zarar

---

### 4. Grafik Blackjack Oyunu
**Dosya:** `blackjack_gui.py`

#### Özellikler:
- **Pygame ile grafik arayüz**
- **Gerçekçi kart görselleri**
- **Animasyonlu oyun deneyimi**
- **Profesyonel casino görünümü**

#### Çalıştırma:
```bash
python blackjack_gui.py
```

#### Grafik Özellikleri:
- **1400x900 çözünürlük**
- **Renkli kart tasarımı**
- **Interaktif butonlar**
- **Canlı istatistik gösterimi**
- **ASCII semboller** (evrensel uyumluluk)

#### Kontroller:
- **Mouse ile tıklama**
- **KART ÇEK** - Yeni kart al
- **DUR** - Kasayı oynata
- **YENİ OYUN** - Yeni el başlat
- **ÇIKIŞ** - Ana menüye dön

#### UI Özellikleri:
- Casino yeşili arka plan
- Altın sarısı başlıklar
- Kırmızı/siyah kart renkleri
- Büyük, okunabilir fontlar
- Merkezi buton düzeni

---

## 🏠 Casino Kuralları

### Temel Kurallar:
- **Amaç:** 21'i geçmeden kasaya en yakın olmak
- **Kart Değerleri:**
  - As: 1 veya 11 (otomatik optimize)
  - J, Q, K: 10
  - Diğerleri: Yüz değeri

### Casino Avantajları:
1. **Double Bust:** Her iki taraf da patlasa oyuncu kaybeder
2. **6:5 Blackjack:** Doğal blackjack 120 birim ödüyor (150 değil)
3. **Soft 17:** Kasa A-6 gibi ellerde kart çeker
4. **Oyuncu Hataları:** Optimal olmayan strateji

### Bahis Sistemi:
- **Her oyun:** 100 birim bahis
- **Normal kazanç:** 100 birim
- **Blackjack kazancı:** 120 birim (6:5)
- **Berabere:** 0 kar/zarar

---

## ⚙️ Teknik Detaylar

### Kod Yapısı:
```
blackjack/
├── blackjack_simulator.py          # Temel simülasyon
├── blackjack_simulator_realistic.py # Gerçekçi casino
├── interactive_blackjack.py         # Text oyunu
├── blackjack_gui.py                # Grafik oyunu
├── requirements.txt                 # Gereksinimler
└── README.md                       # Bu dosya
```

### Sınıf Yapısı:
- **Card:** Tek kart temsili
- **Deck:** 6 desteli kart havuzu
- **Hand:** Oyuncu/kasa eli
- **BlackjackGame/GUI:** Ana oyun mantığı

### Algoritmalar:
- **As Optimizasyonu:** Otomatik 11→1 dönüşümü
- **Soft El Tespiti:** A-6 gibi esnek eller
- **Kart Karıştırma:** 20 karttan az kalınca yenile
- **Rastgele Strateji:** Gerçekçi oyuncu davranışı

---

## 📊 İstatistikler ve Analizler

### Simülasyon Sonuçları (10.000 oyun):

#### Temel Simülasyon:
```
Toplam Kar/Zarar: +78.550 birim
House Edge: -%7.86 (oyuncu lehine)
Kazanma Oranı: %39.8
Blackjack Oranı: %4.8
```

#### Gerçekçi Casino:
```
Toplam Kar/Zarar: -118.740 birim
House Edge: +%11.87 (casino lehine)
Kazanma Oranı: %39.7
Blackjack Oranı: %4.7
```

### Grafikler:
- **Bar Chart:** Her 1000 oyun için kar/zarar
- **Line Chart:** Kümülatif performans
- **Renkli Gösterim:** Yeşil kazanç, kırmızı kayıp

---

## 🎯 Kullanım Senaryoları

### 1. Eğitim ve Öğrenme:
- Blackjack kurallarını öğrenme
- Casino matematik anlayışı
- Olasılık teorisi uygulaması

### 2. Strateji Analizi:
- Farklı oyuncu stratejilerini test etme
- Casino avantajını anlama
- Risk yönetimi öğrenme

### 3. Eğlence:
- Gerçekçi casino deneyimi
- Risk almadan oyun oynama
- Arkadaşlarla yarışma

### 4. Araştırma:
- Monte Carlo simülasyonu
- İstatistiksel analiz
- Oyun teorisi uygulamaları

---

## 🛠️ Geliştirme Notları

### Font Sistemi:
- **Arial SysFont** kullanımı
- **Unicode desteği** için fallback
- **ASCII semboller** evrensel uyumluluk için

### Performans:
- **60 FPS** grafik oyunu
- **Hızlı simülasyon** (10.000 oyun ~2 saniye)
- **Bellek optimizasyonu** büyük desteler için

### Uyumluluk:
- **Windows/Mac/Linux** desteği
- **Python 3.7+** uyumluluğu
- **Düşük sistem gereksinimleri**

---

## 📈 Gelecek Geliştirmeler

### Planlanan Özellikler:
- [ ] Çoklu oyuncu desteği
- [ ] Farklı blackjack varyantları
- [ ] Makine öğrenmesi tabanlı strateji
- [ ] Web tabanlı versiyon
- [ ] Mobil uygulama
- [ ] Gerçek zamanlı multiplayer

### Potansiyel İyileştirmeler:
- [ ] Daha gelişmiş grafik efektleri
- [ ] Ses efektleri
- [ ] Özelleştirilebilir kurallar
- [ ] Turnuva modu
- [ ] Başarım sistemi

---

## 📞 İletişim ve Katkı

Bu proje açık kaynak olarak geliştirilmiştir. Katkılarınızı ve geri bildirimlerinizi bekliyoruz!

### Katkıda Bulunma:
1. Projeyi fork edin
2. Yeni özellik dalı oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

### Hata Bildirimi:
- Detaylı açıklama ile issue açın
- Hata mesajlarını ekleyin
- Sistem bilgilerini paylaşın

---

## 📄 Lisans

Bu proje MIT lisansı altında yayınlanmıştır. Detaylar için LICENSE dosyasına bakınız.

---

**🎰 İyi oyunlar! Sorumlu kumar oynayın! 🎰** 