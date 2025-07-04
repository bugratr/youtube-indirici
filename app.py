#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YouTube Video İndirici - Web Arayüzü
Flask ile web tabanlı YouTube video indirme servisi
"""

import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from flask_cors import CORS
from youtube_downloader import YouTubeDownloader
import threading
import time

app = Flask(__name__)
app.secret_key = 'youtube_downloader_secret_key_2024'
CORS(app)

# Global değişkenler
download_status = {}
downloader = YouTubeDownloader()

def background_download(url, quality, audio_only, task_id):
    """Arka planda video indirme"""
    try:
        download_status[task_id] = {
            'status': 'downloading',
            'message': 'İndiriliyor...',
            'progress': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        success, message = downloader.download_video(url, quality=quality, audio_only=audio_only)
        
        if success:
            download_status[task_id] = {
                'status': 'completed',
                'message': 'İndirme tamamlandı!',
                'progress': 100,
                'timestamp': datetime.now().isoformat()
            }
        else:
            download_status[task_id] = {
                'status': 'failed',
                'message': message,
                'progress': 0,
                'timestamp': datetime.now().isoformat()
            }
    except Exception as e:
        download_status[task_id] = {
            'status': 'failed',
            'message': f'Hata: {str(e)}',
            'progress': 0,
            'timestamp': datetime.now().isoformat()
        }

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/validate_url', methods=['POST'])
def validate_url():
    """URL doğrulama"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'valid': False, 'message': 'URL boş olamaz!'})
    
    if not downloader.is_valid_youtube_url(url):
        return jsonify({'valid': False, 'message': 'Geçersiz YouTube URL!'})
    
    return jsonify({'valid': True, 'message': 'URL geçerli!'})

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    """Video bilgilerini getir"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url or not downloader.is_valid_youtube_url(url):
        return jsonify({'success': False, 'message': 'Geçersiz URL!'})
    
    try:
        info = downloader.get_video_info(url)
        
        if info:
            return jsonify({
                'success': True,
                'info': {
                    'title': info['title'],
                    'duration': downloader.format_duration(info['duration']),
                    'view_count': downloader.format_view_count(info['view_count']),
                    'uploader': info['uploader'],
                    'upload_date': info['upload_date'],
                    'description': info['description']
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Video bilgileri alınamadı!'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Hata: {str(e)}'})

@app.route('/download', methods=['POST'])
def download():
    """Video indirme"""
    data = request.get_json()
    url = data.get('url', '').strip()
    quality = data.get('quality', 'best')
    audio_only = data.get('audio_only', False)
    
    if not url or not downloader.is_valid_youtube_url(url):
        return jsonify({'success': False, 'message': 'Geçersiz URL!'})
    
    # Benzersiz görev ID'si oluştur
    task_id = f"download_{int(time.time() * 1000)}"
    
    # Arka planda indirme başlat
    thread = threading.Thread(
        target=background_download,
        args=(url, quality, audio_only, task_id)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'task_id': task_id,
        'message': 'İndirme başlatıldı!'
    })

@app.route('/download_status/<task_id>')
def get_download_status(task_id):
    """İndirme durumunu getir"""
    status = download_status.get(task_id, {
        'status': 'not_found',
        'message': 'Görev bulunamadı!',
        'progress': 0
    })
    
    return jsonify(status)

@app.route('/downloads')
def list_downloads():
    """İndirilen dosyaları listele"""
    downloads_dir = Path('downloads')
    
    if not downloads_dir.exists():
        return jsonify({'files': []})
    
    files = []
    for file_path in downloads_dir.glob('*'):
        if file_path.is_file():
            stat = file_path.stat()
            files.append({
                'name': file_path.name,
                'size': f"{stat.st_size / (1024*1024):.2f} MB",
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    
    # Değişiklik tarihine göre sırala
    files.sort(key=lambda x: x['modified'], reverse=True)
    
    return jsonify({'files': files})

@app.route('/download_file/<filename>')
def download_file(filename):
    """Dosya indirme"""
    file_path = Path('downloads') / filename
    
    if not file_path.exists():
        return jsonify({'error': 'Dosya bulunamadı!'}), 404
    
    return send_file(file_path, as_attachment=True)

@app.route('/delete_file/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Dosya silme"""
    file_path = Path('downloads') / filename
    
    if not file_path.exists():
        return jsonify({'success': False, 'message': 'Dosya bulunamadı!'})
    
    try:
        file_path.unlink()
        return jsonify({'success': True, 'message': 'Dosya silindi!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Silme hatası: {str(e)}'})

@app.route('/health')
def health_check():
    """Sağlık kontrolü"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Downloads klasörünü oluştur
    Path('downloads').mkdir(exist_ok=True)
    
    print("🚀 YouTube Video İndirici Web Servisi Başlatılıyor...")
    print("🌐 Tarayıcınızda http://localhost:5000 adresini açın")
    print("⏹️  Durdurmak için Ctrl+C tuşlarına basın")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 