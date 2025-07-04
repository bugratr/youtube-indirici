#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YouTube Video İndirici - Hızlı Test Scripti
Bu script temel fonksiyonların çalışıp çalışmadığını test eder.
"""

import sys
import os
from youtube_downloader import YouTubeDownloader

def test_url_validation():
    """URL doğrulama testleri"""
    print("🔍 URL Doğrulama Testi...")
    
    downloader = YouTubeDownloader()
    
    # Test URL'leri
    test_urls = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
        ("https://youtu.be/dQw4w9WgXcQ", True),
        ("https://youtube.com/watch?v=dQw4w9WgXcQ", True),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", True),
        ("https://www.google.com", False),
        ("not_a_url", False),
        ("", False),
    ]
    
    for url, expected in test_urls:
        result = downloader.is_valid_youtube_url(url)
        status = "✅" if result == expected else "❌"
        print(f"{status} {url[:50]}{'...' if len(url) > 50 else ''} -> {result}")
    
    print()

def test_video_info():
    """Video bilgilerini getirme testi"""
    print("📊 Video Bilgisi Testi...")
    
    downloader = YouTubeDownloader()
    
    # Test URL'si (Rick Astley - Never Gonna Give You Up)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"Test URL: {test_url}")
    
    try:
        info = downloader.get_video_info(test_url)
        
        if info:
            print("✅ Video bilgileri başarıyla alındı!")
            print(f"📺 Başlık: {info['title']}")
            print(f"⏱️  Süre: {downloader.format_duration(info['duration'])}")
            print(f"👁️  Görüntülenme: {downloader.format_view_count(info['view_count'])}")
            print(f"👤 Kanal: {info['uploader']}")
            print(f"📅 Tarih: {info['upload_date']}")
        else:
            print("❌ Video bilgileri alınamadı!")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    print()

def test_format_functions():
    """Format fonksiyonlarını test et"""
    print("🔧 Format Fonksiyonları Testi...")
    
    downloader = YouTubeDownloader()
    
    # Süre formatı testleri
    duration_tests = [
        (0, "Bilinmeyen"),
        (30, "0:30"),
        (90, "1:30"),
        (3661, "1:01:01"),
    ]
    
    print("⏱️  Süre Formatı Testi:")
    for seconds, expected in duration_tests:
        result = downloader.format_duration(seconds)
        status = "✅" if result == expected else "❌"
        print(f"{status} {seconds} saniye -> {result}")
    
    # Görüntülenme sayısı formatı testleri
    view_tests = [
        (0, "Bilinmeyen"),
        (500, "500"),
        (1500, "1.5K"),
        (1500000, "1.5M"),
    ]
    
    print("\n👁️  Görüntülenme Formatı Testi:")
    for count, expected in view_tests:
        result = downloader.format_view_count(count)
        status = "✅" if result == expected else "❌"
        print(f"{status} {count} -> {result}")
    
    print()

def test_download_path():
    """İndirme klasörü testi"""
    print("📁 İndirme Klasörü Testi...")
    
    downloader = YouTubeDownloader()
    
    if downloader.download_path.exists():
        print("✅ İndirme klasörü başarıyla oluşturuldu!")
        print(f"📁 Klasör yolu: {downloader.download_path}")
    else:
        print("❌ İndirme klasörü oluşturulamadı!")
    
    print()

def main():
    """Ana test fonksiyonu"""
    print("=" * 60)
    print("🧪 YouTube Video İndirici - Hızlı Test")
    print("=" * 60)
    print()
    
    try:
        # Temel testler
        test_url_validation()
        test_format_functions()
        test_download_path()
        
        # İnternet bağlantısı gerektiren test
        print("🌐 İnternet Bağlantısı Testi...")
        response = input("İnternet bağlantısı testi yapmak ister misiniz? (e/h): ").strip().lower()
        
        if response in ['e', 'evet', 'y', 'yes']:
            test_video_info()
        else:
            print("⏭️  İnternet testi atlandı.")
            print()
        
        print("=" * 60)
        print("🎉 Tüm testler tamamlandı!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n👋 Test kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Test sırasında hata: {e}")

if __name__ == "__main__":
    main() 