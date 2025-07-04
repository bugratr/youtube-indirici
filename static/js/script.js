// YouTube Video İndirici - JavaScript Fonksiyonları

// Global değişkenler
let currentTaskId = null;
let progressInterval = null;

// Yardımcı fonksiyonlar
function showElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'block';
        element.classList.add('fade-in');
    }
}

function hideElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'none';
        element.classList.remove('fade-in');
    }
}

function showFeedback(message, type = 'info') {
    const feedback = document.getElementById('url-feedback');
    feedback.innerHTML = `
        <div class="feedback-message feedback-${type}">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-times-circle' : 'fa-info-circle'} me-2"></i>
            ${message}
        </div>
    `;
    feedback.classList.add('fade-in');
}

function clearFeedback() {
    const feedback = document.getElementById('url-feedback');
    feedback.innerHTML = '';
    feedback.classList.remove('fade-in');
}

function showLoading(buttonId) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="loading-spinner me-2"></span>Yükleniyor...';
    }
}

function hideLoading(buttonId, originalText) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = false;
        button.innerHTML = originalText;
    }
}

// URL doğrulama fonksiyonu
async function validateUrl(url) {
    try {
        const response = await fetch('/validate_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();
        
        if (data.valid) {
            showFeedback(data.message, 'success');
        } else {
            showFeedback(data.message, 'error');
            hideVideoInfo();
        }
        
        return data.valid;
    } catch (error) {
        showFeedback('URL doğrulama hatası: ' + error.message, 'error');
        return false;
    }
}

// Video bilgilerini alma fonksiyonu
async function getVideoInfo(url) {
    showLoading('get-info-btn');
    
    try {
        const response = await fetch('/get_video_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();
        
        if (data.success) {
            displayVideoInfo(data.info);
            showDownloadOptions();
            showFeedback('Video bilgileri başarıyla alındı!', 'success');
        } else {
            showFeedback('Video bilgileri alınamadı: ' + data.message, 'error');
            hideVideoInfo();
        }
    } catch (error) {
        showFeedback('Video bilgilerini alırken hata: ' + error.message, 'error');
        hideVideoInfo();
    } finally {
        hideLoading('get-info-btn', '<i class="fas fa-search me-1"></i>Bilgi Al');
    }
}

// Video bilgilerini görüntüleme
function displayVideoInfo(info) {
    const videoInfoContent = document.getElementById('video-info-content');
    videoInfoContent.innerHTML = `
        <div class="video-info">
            <div class="video-title">${info.title}</div>
            <div class="row">
                <div class="col-md-6">
                    <h6>Süre</h6>
                    <p><i class="fas fa-clock me-2"></i>${info.duration}</p>
                </div>
                <div class="col-md-6">
                    <h6>Görüntülenme</h6>
                    <p><i class="fas fa-eye me-2"></i>${info.view_count}</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <h6>Kanal</h6>
                    <p><i class="fas fa-user me-2"></i>${info.uploader}</p>
                </div>
                <div class="col-md-6">
                    <h6>Yayın Tarihi</h6>
                    <p><i class="fas fa-calendar me-2"></i>${info.upload_date}</p>
                </div>
            </div>
            <div>
                <h6>Açıklama</h6>
                <p><i class="fas fa-info me-2"></i>${info.description}</p>
            </div>
        </div>
    `;
    
    showElement('video-info-section');
}

// Video bilgilerini gizleme
function hideVideoInfo() {
    hideElement('video-info-section');
    hideElement('download-options-section');
}

// İndirme seçeneklerini gösterme
function showDownloadOptions() {
    showElement('download-options-section');
}

// İndirme başlatma
async function startDownload(url, downloadType, quality) {
    const audioOnly = downloadType === 'audio';
    
    showLoading('download-btn');
    
    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                quality: quality,
                audio_only: audioOnly
            })
        });

        const data = await response.json();
        
        if (data.success) {
            currentTaskId = data.task_id;
            showDownloadProgress();
            startProgressTracking();
            showFeedback('İndirme başlatıldı!', 'success');
        } else {
            showFeedback('İndirme hatası: ' + data.message, 'error');
        }
    } catch (error) {
        showFeedback('İndirme başlatılırken hata: ' + error.message, 'error');
    } finally {
        hideLoading('download-btn', '<i class="fas fa-download me-2"></i>İndir');
    }
}

// İndirme ilerlemesini gösterme
function showDownloadProgress() {
    showElement('download-progress-section');
    
    // Progress bar'ı sıfırla
    const progressBar = document.getElementById('download-progress');
    const statusDiv = document.getElementById('download-status');
    
    progressBar.style.width = '0%';
    progressBar.textContent = '0%';
    statusDiv.textContent = 'İndirme başlatılıyor...';
}

// İlerleme takibi başlatma
function startProgressTracking() {
    if (progressInterval) {
        clearInterval(progressInterval);
    }
    
    progressInterval = setInterval(async () => {
        if (currentTaskId) {
            await checkDownloadStatus();
        }
    }, 2000); // Her 2 saniyede bir kontrol et
}

// İndirme durumunu kontrol etme
async function checkDownloadStatus() {
    try {
        const response = await fetch(`/download_status/${currentTaskId}`);
        const data = await response.json();
        
        const progressBar = document.getElementById('download-progress');
        const statusDiv = document.getElementById('download-status');
        
        // Progress bar'ı güncelle
        progressBar.style.width = `${data.progress}%`;
        progressBar.textContent = `${data.progress}%`;
        
        // Durum mesajını güncelle
        statusDiv.textContent = data.message;
        
        // İndirme tamamlandıysa veya hata varsa
        if (data.status === 'completed' || data.status === 'failed') {
            clearInterval(progressInterval);
            currentTaskId = null;
            
            if (data.status === 'completed') {
                progressBar.classList.remove('progress-bar-striped', 'progress-bar-animated');
                progressBar.classList.add('bg-success');
                statusDiv.innerHTML = '<i class="fas fa-check-circle text-success me-2"></i>' + data.message;
                
                // İndirilen dosyaları yeniden yükle
                setTimeout(() => {
                    loadDownloads();
                }, 1000);
            } else {
                progressBar.classList.remove('progress-bar-striped', 'progress-bar-animated');
                progressBar.classList.add('bg-danger');
                statusDiv.innerHTML = '<i class="fas fa-times-circle text-danger me-2"></i>' + data.message;
            }
        }
    } catch (error) {
        console.error('İndirme durumu kontrol hatası:', error);
    }
}

// İndirilen dosyaları yükleme
async function loadDownloads() {
    try {
        const response = await fetch('/downloads');
        const data = await response.json();
        
        displayDownloads(data.files);
    } catch (error) {
        console.error('İndirilen dosyalar yüklenirken hata:', error);
    }
}

// İndirilen dosyaları görüntüleme
function displayDownloads(files) {
    const downloadsList = document.getElementById('downloads-list');
    
    if (files.length === 0) {
        downloadsList.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="fas fa-folder-open fa-3x mb-3"></i>
                <p>Henüz indirilen dosya bulunmuyor.</p>
            </div>
        `;
        return;
    }
    
    let html = '<div class="downloads-list">';
    
    files.forEach(file => {
        const fileIcon = file.name.endsWith('.mp3') ? 'fa-music' : 'fa-video';
        const fileColor = file.name.endsWith('.mp3') ? 'text-success' : 'text-primary';
        
        html += `
            <div class="download-item">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="file-name">
                            <i class="fas ${fileIcon} ${fileColor} me-2"></i>
                            ${file.name}
                        </div>
                        <div class="file-info">
                            <span class="me-3"><i class="fas fa-hdd me-1"></i>${file.size}</span>
                            <span><i class="fas fa-calendar me-1"></i>${file.modified}</span>
                        </div>
                    </div>
                    <div class="file-actions">
                        <button class="btn btn-primary btn-sm" onclick="downloadFile('${file.name}')">
                            <i class="fas fa-download me-1"></i>İndir
                        </button>
                        <button class="btn btn-danger btn-sm" onclick="deleteFile('${file.name}')">
                            <i class="fas fa-trash me-1"></i>Sil
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    downloadsList.innerHTML = html;
}

// Dosya indirme
function downloadFile(filename) {
    window.open(`/download_file/${encodeURIComponent(filename)}`, '_blank');
}

// Dosya silme
async function deleteFile(filename) {
    if (!confirm(`"${filename}" dosyasını silmek istediğinizden emin misiniz?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/delete_file/${encodeURIComponent(filename)}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showFeedback('Dosya başarıyla silindi!', 'success');
            loadDownloads(); // Listeyi yenile
        } else {
            showFeedback('Dosya silinirken hata: ' + data.message, 'error');
        }
    } catch (error) {
        showFeedback('Dosya silinirken hata: ' + error.message, 'error');
    }
}

// İndirilen dosyaları gösterme/gizleme
function showDownloads() {
    const downloadsSection = document.getElementById('downloads-list-section');
    
    if (downloadsSection.style.display === 'none' || !downloadsSection.style.display) {
        showElement('downloads-list-section');
        loadDownloads();
    } else {
        hideElement('downloads-list-section');
    }
}

// Sayfa yüklendiğinde çalışacak fonksiyonlar
document.addEventListener('DOMContentLoaded', function() {
    // URL input'a enter tuşu ile bilgi alma
    document.getElementById('video-url').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const url = this.value.trim();
            if (url) {
                getVideoInfo(url);
            }
        }
    });
    
    // Download button'a enter tuşu ile indirme
    document.getElementById('download-btn').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            this.click();
        }
    });
    
    // URL input'a paste olayı
    document.getElementById('video-url').addEventListener('paste', function(e) {
        setTimeout(() => {
            const url = this.value.trim();
            if (url) {
                validateUrl(url);
            }
        }, 100);
    });
    
    // İndirme türü değiştiğinde kalite seçimini göster/gizle
    document.querySelectorAll('input[name="download-type"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const qualitySection = document.getElementById('quality-section');
            if (this.value === 'audio') {
                qualitySection.style.display = 'none';
            } else {
                qualitySection.style.display = 'block';
            }
        });
    });
});

// Sayfa kapanırken interval'leri temizle
window.addEventListener('beforeunload', function() {
    if (progressInterval) {
        clearInterval(progressInterval);
    }
});

// Hata durumunda console'a log
window.addEventListener('error', function(e) {
    console.error('JavaScript Hatası:', e.error);
});

// Service Worker kaydı (offline destek için)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('Service Worker başarıyla kaydedildi:', registration.scope);
            })
            .catch(function(error) {
                console.log('Service Worker kaydı başarısız:', error);
            });
    });
}

// Tema değiştirme (dark/light mode)
function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.contains('dark-theme');
    
    if (isDark) {
        body.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
    }
}

// Sayfa yüklendiğinde tema ayarını uygula
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
});

// Klavye kısayolları
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter ile indirme başlat
    if (e.ctrlKey && e.key === 'Enter') {
        const downloadBtn = document.getElementById('download-btn');
        if (downloadBtn && !downloadBtn.disabled) {
            downloadBtn.click();
        }
    }
    
    // Escape ile progress'i gizle
    if (e.key === 'Escape') {
        hideElement('download-progress-section');
        if (progressInterval) {
            clearInterval(progressInterval);
        }
    }
});

// Dosya sürükle bırak desteği
document.addEventListener('dragover', function(e) {
    e.preventDefault();
});

document.addEventListener('drop', function(e) {
    e.preventDefault();
    const files = e.dataTransfer.files;
    
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'text/plain') {
            const reader = new FileReader();
            reader.onload = function(e) {
                const content = e.target.result;
                const urls = content.split('\n').filter(line => line.trim());
                
                if (urls.length > 0) {
                    document.getElementById('video-url').value = urls[0].trim();
                    validateUrl(urls[0].trim());
                }
            };
            reader.readAsText(file);
        }
    }
});

// Responsive menu toggle
function toggleMobileMenu() {
    const navbarCollapse = document.querySelector('.navbar-collapse');
    navbarCollapse.classList.toggle('show');
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Loading animation for buttons
function animateButton(buttonId) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.classList.add('pulse');
        setTimeout(() => {
            button.classList.remove('pulse');
        }, 1000);
    }
}

// Toast notification sistemi
function showToast(message, type = 'info', duration = 3000) {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-times-circle' : 'fa-info-circle'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Otomatik silme
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, duration);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
} 