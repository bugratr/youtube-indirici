#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
from pathlib import Path
import yt_dlp
from urllib.parse import urlparse


class YouTubeDownloader:
    def __init__(self, download_path="downloads"):
        """
        YouTube video indirici sınıfı
        
        Args:
            download_path (str): Videoların indirileceği klasör yolu
        """
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        
    def is_valid_youtube_url(self, url):
        """
        YouTube URL'sinin geçerli olup olmadığını kontrol eder
        
        Args:
            url (str): Kontrol edilecek URL
            
        Returns:
            bool: URL geçerli ise True, değilse False
        """
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        return youtube_regex.match(url) is not None
    
    def get_video_info(self, url):
        """
        Video bilgilerini getirir
        
        Args:
            url (str): YouTube video URL'si
            
        Returns:
            dict: Video bilgileri
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Bilinmeyen Başlık'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'uploader': info.get('uploader', 'Bilinmeyen'),
                    'upload_date': info.get('upload_date', 'Bilinmeyen'),
                    'description': info.get('description', '')[:200] + '...' if info.get('description') else 'Açıklama yok'
                }
        except Exception as e:
            return None
    
    def download_video(self, url, quality='best', audio_only=False):
        """
        YouTube videosunu indirir
        
        Args:
            url (str): YouTube video URL'si
            quality (str): Video kalitesi ('best', 'worst', '720p', '480p', vb.)
            audio_only (bool): Sadece ses dosyası indir
            
        Returns:
            tuple: (başarılı_mı, mesaj)
        """
        try:
            if audio_only:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
            else:
                # Video kalitesi ayarları
                if quality == 'best':
                    format_selector = 'best[ext=mp4]'
                elif quality == 'worst':
                    format_selector = 'worst[ext=mp4]'
                elif quality.endswith('p'):
                    height = quality[:-1]
                    format_selector = f'best[height<={height}][ext=mp4]'
                else:
                    format_selector = 'best[ext=mp4]'
                
                ydl_opts = {
                    'format': format_selector,
                    'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            return True, "Video başarıyla indirildi!"
            
        except Exception as e:
            return False, f"İndirme hatası: {str(e)}"
    
    def format_duration(self, seconds):
        """
        Saniyeyi dakika:saniye formatına çevirir
        
        Args:
            seconds (int): Saniye cinsinden süre
            
        Returns:
            str: Formatlanmış süre
        """
        if seconds == 0:
            return "Bilinmeyen"
        
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def format_view_count(self, count):
        """
        Görüntülenme sayısını formatlar
        
        Args:
            count (int): Görüntülenme sayısı
            
        Returns:
            str: Formatlanmış görüntülenme sayısı
        """
        if count == 0:
            return "Bilinmeyen"
        
        if count >= 1000000:
            return f"{count / 1000000:.1f}M"
        elif count >= 1000:
            return f"{count / 1000:.1f}K"
        else:
            return str(count)


def main():
    """Ana uygulama fonksiyonu"""
    print("=" * 60)
    print("🎬 YouTube Video İndirici")
    print("=" * 60)
    
    downloader = YouTubeDownloader()
    
    while True:
        print("\n📹 YouTube Video İndirici Menüsü:")
        print("1. Video İndir")
        print("2. Sadece Ses İndir (MP3)")
        print("3. Çıkış")
        
        choice = input("\nSeçiminizi yapın (1-3): ").strip()
        
        if choice == '3':
            print("\nGüle güle! 👋")
            break
        
        if choice not in ['1', '2']:
            print("❌ Geçersiz seçim! Lütfen 1-3 arasında bir sayı girin.")
            continue
        
        # URL girişi
        url = input("\n🔗 YouTube video URL'sini girin: ").strip()
        
        if not url:
            print("❌ URL boş olamaz!")
            continue
        
        if not downloader.is_valid_youtube_url(url):
            print("❌ Geçersiz YouTube URL'si!")
            continue
        
        # Video bilgilerini getir
        print("\n📊 Video bilgileri getiriliyor...")
        video_info = downloader.get_video_info(url)
        
        if not video_info:
            print("❌ Video bilgileri alınamadı!")
            continue
        
        # Video bilgilerini göster
        print("\n" + "=" * 60)
        print(f"📺 Başlık: {video_info['title']}")
        print(f"⏱️  Süre: {downloader.format_duration(video_info['duration'])}")
        print(f"👁️  Görüntülenme: {downloader.format_view_count(video_info['view_count'])}")
        print(f"👤 Kanal: {video_info['uploader']}")
        print(f"📅 Tarih: {video_info['upload_date']}")
        print(f"📝 Açıklama: {video_info['description']}")
        print("=" * 60)
        
        # İndirme onayı
        confirm = input("\n✅ Bu videoyu indirmek istediğinizden emin misiniz? (e/h): ").strip().lower()
        
        if confirm not in ['e', 'evet', 'y', 'yes']:
            print("❌ İndirme iptal edildi.")
            continue
        
        # İndirme işlemi
        if choice == '1':  # Video indirme
            print("\n🎬 Video kalitesi seçin:")
            print("1. En iyi kalite")
            print("2. 720p")
            print("3. 480p")
            print("4. 360p")
            print("5. En düşük kalite")
            
            quality_choice = input("\nKalite seçin (1-5): ").strip()
            
            quality_map = {
                '1': 'best',
                '2': '720p',
                '3': '480p',
                '4': '360p',
                '5': 'worst'
            }
            
            quality = quality_map.get(quality_choice, 'best')
            
            print(f"\n⬇️  Video indiriliyor ({quality} kalite)...")
            success, message = downloader.download_video(url, quality=quality)
            
        else:  # Ses indirme
            print("\n🎵 Ses dosyası (MP3) indiriliyor...")
            success, message = downloader.download_video(url, audio_only=True)
        
        # Sonucu göster
        if success:
            print(f"\n✅ {message}")
            print(f"📁 Dosya konumu: {downloader.download_path}")
        else:
            print(f"\n❌ {message}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Uygulama kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {str(e)}") 