# 🎬 YouTube Video İndirici

Python ile yazılmış modern web arayüzlü YouTube video indirme uygulaması. Bu uygulama ile YouTube videolarını MP4 formatında veya sadece ses dosyalarını MP3 formatında indirebilirsiniz.

## ✨ Özellikler

- 🌐 **Web Arayüzü**: Modern, responsive ve kullanıcı dostu web arayüzü
- ✅ **YouTube Video İndirme**: MP4 formatında video indirme
- 🎵 **Ses İndirme**: MP3 formatında sadece ses dosyası indirme
- 🎯 **Kalite Seçimi**: En iyi, 720p, 480p, 360p, en düşük kalite seçenekleri
- 📊 **Video Bilgileri**: Başlık, süre, görüntülenme sayısı, kanal bilgisi
- 🔒 **URL Doğrulama**: Gerçek zamanlı URL geçerlilik kontrolü
- 📁 **Dosya Yönetimi**: İndirilen dosyaları görüntüleme, indirme ve silme
- 🔄 **Canlı İlerleme**: Gerçek zamanlı indirme durumu takibi
- 📱 **Responsive Tasarım**: Mobil ve masaüstü uyumlu
- 💻 **Komut Satırı**: Terminal tabanlı alternatif kullanım

## 🛠️ Kurulum

### 1. Gereksinimler

- Python 3.6 veya üzeri
- pip (Python paket yöneticisi)

### 2. Bağımlılıkları Yükleme

```bash
pip install -r requirements.txt
```

### 3. FFmpeg Kurulumu (MP3 dönüşümü için)

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
1. [FFmpeg indirme sayfasından](https://ffmpeg.org/download.html) indirin
2. Sistem PATH'ine ekleyin

## 🚀 Kullanım

### Web Arayüzü (Önerilen)

1. **Web Servisini Başlatın:**
```bash
python app.py
```

2. **Tarayıcıda Açın:**
```
http://localhost:5000
```

3. **YouTube URL'sini Girin:**
- URL kutusuna YouTube linkini yapıştırın
- "Bilgi Al" butonuna tıklayın

4. **Video Bilgilerini Görüntüleyin:**
- Video başlığı, süresi, görüntülenme sayısı
- Kanal bilgisi ve yayın tarihi

5. **İndirme Seçeneklerini Belirleyin:**
- Video (MP4) veya Ses (MP3) seçin
- Kalite seçimi yapın (sadece video için)

6. **İndirin:**
- "İndir" butonuna tıklayın
- İndirme ilerlemesini takip edin

### Komut Satırı (Terminal)

```bash
python youtube_downloader.py
```

## 📁 Dosya Yapısı

```
youtube2mp4/
├── app.py                    # Web uygulaması (Flask)
├── youtube_downloader.py     # Ana indirme sınıfı
├── requirements.txt          # Python bağımlılıkları
├── README.md                # Kullanım kılavuzu
├── quick_test.py            # Test scripti
├── templates/               # HTML şablonları
│   ├── base.html           # Temel şablon
│   └── index.html          # Ana sayfa
├── static/                  # Statik dosyalar
│   ├── css/
│   │   └── style.css       # Özel CSS stilleri
│   └── js/
│       └── script.js       # JavaScript işlevleri
└── downloads/              # İndirilen dosyalar (otomatik oluşturulur)
```

## 🌐 Web Arayüzü Özellikleri

### 🎨 Modern Tasarım
- Gradient renkler ve animasyonlar
- Responsive Bootstrap 5 tasarımı
- Font Awesome ikonları
- Karanlık mod desteği

### 🔧 Gelişmiş Özellikler
- **Gerçek zamanlı URL doğrulama**
- **Canlı indirme ilerlemesi**
- **Dosya yönetimi sistemi**
- **Klavye kısayolları** (Ctrl+Enter ile indirme)
- **Sürükle-bırak desteği**
- **Toast bildirimleri**

### 📱 Mobil Destek
- Tam responsive tasarım
- Dokunmatik ekran optimizasyonu
- Mobil menü sistemi

## 🔌 API Endpoints

### Video İşlemleri
- `POST /validate_url` - URL doğrulama
- `POST /get_video_info` - Video bilgileri alma
- `POST /download` - İndirme başlatma
- `GET /download_status/<task_id>` - İndirme durumu

### Dosya İşlemleri
- `GET /downloads` - İndirilen dosyaları listele
- `GET /download_file/<filename>` - Dosya indirme
- `DELETE /delete_file/<filename>` - Dosya silme

### Sistem
- `GET /health` - Sistem durumu kontrolü

## 📝 Kullanım Örnekleri

### Web Arayüzü
1. **Ana sayfaya gidin:** `http://localhost:5000`
2. **URL girin:** `https://www.youtube.com/watch?v=EXAMPLE`
3. **Video bilgilerini görüntüleyin**
4. **İndirme seçeneklerini belirleyin**
5. **İndirmeyi başlatın**

### Desteklenen URL Formatları
```
✅ https://www.youtube.com/watch?v=VIDEO_ID
✅ https://youtu.be/VIDEO_ID
✅ https://youtube.com/watch?v=VIDEO_ID
✅ https://www.youtube.com/embed/VIDEO_ID
✅ https://m.youtube.com/watch?v=VIDEO_ID
```

## 🧪 Test Etme

### Hızlı Test
```bash
python quick_test.py
```

### Manuel Test
```bash
# Web servisi testi
python app.py

# Komut satırı testi
python youtube_downloader.py
```

## ⚠️ Önemli Notlar

1. **Telif Hakkı**: Bu uygulama yalnızca eğitim amaçlı geliştirilmiştir. Telif hakkı korumalı içerikleri indirmeden önce gerekli izinleri aldığınızdan emin olun.

2. **Yasal Sorumluluk**: İndirilen içeriklerin yasal kullanımı tamamen kullanıcının sorumluluğundadır.

3. **Performans**: Büyük dosyalar için indirme süresi internet hızınıza bağlı olarak değişebilir.

4. **Güvenlik**: Web servisi varsayılan olarak localhost'ta çalışır. Dış erişim için güvenlik ayarları yapılmalıdır.

## 🐛 Sorun Giderme

### FFmpeg Bulunamadı Hatası
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### Port Çakışması
```bash
# Farklı port kullanmak için
python app.py --port 8080
```

### Bağımlılık Hatası
```bash
pip install --upgrade yt-dlp flask flask-cors
```

### İndirme Hatası
1. İnternet bağlantınızı kontrol edin
2. URL'nin doğru olduğundan emin olun
3. Videonun hala erişilebilir olduğunu kontrol edin
4. Yaş sınırlaması veya bölgesel kısıtlama olabilir

## 🔧 Geliştirme

### Teknolojiler
- **Backend**: Python, Flask, yt-dlp
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Veritabanı**: Dosya tabanlı (JSON)
- **API**: RESTful API

### Kod Yapısı
```python
# Ana sınıflar
YouTubeDownloader    # Video indirme işlemleri
Flask App           # Web servisi
JavaScript API      # Frontend etkileşimleri
```

### Özellik Ekleme
1. `app.py` - Backend endpoint'leri
2. `templates/` - HTML şablonları
3. `static/` - CSS/JS dosyaları
4. `youtube_downloader.py` - Çekirdek işlevsellik

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Yeni özellik dalı oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Dalınızı push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📊 Sistem Gereksinimleri

- **Python**: 3.6+
- **RAM**: En az 512 MB
- **Disk**: İndirilen video boyutuna bağlı
- **İnternet**: Aktif bağlantı gerekli
- **Tarayıcı**: Modern tarayıcı (Chrome, Firefox, Safari, Edge)

## 🔒 Güvenlik

- **CORS**: Kontrollü kaynak paylaşımı
- **Input Validation**: URL ve form doğrulaması
- **File Security**: Güvenli dosya işlemleri
- **Error Handling**: Kapsamlı hata yönetimi

## 📜 Lisans

Bu proje MIT lisansı altında yayınlanmıştır.

## 🎯 Gelecek Özellikler

- [ ] Toplu indirme desteği
- [ ] Oynatma listesi indirme
- [ ] Video önizleme
- [ ] İndirme geçmişi
- [ ] Kullanıcı hesapları
- [ ] Tema özelleştirme
- [ ] Mobil uygulama

---

**Not**: Bu uygulama sadece eğitim amaçlıdır. YouTube'un hizmet şartlarına ve telif hakkı yasalarına uygun kullanın.

## 📞 Destek

Sorun yaşıyorsanız:
1. [Issues](https://github.com/your-repo/issues) bölümünden bildirebilirsiniz
2. `quick_test.py` ile sistem testini çalıştırın
3. Console log'larını kontrol edin

---

🚀 **Hızlı Başlangıç**: `python app.py` komutu ile web arayüzünü başlatın ve `http://localhost:5000` adresini ziyaret edin! 