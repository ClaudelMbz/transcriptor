#!/usr/bin/env python3
"""
Application web Flask pour transcrire des vidéos YouTube et TikTok
"""

from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os
import tempfile
import threading

app = Flask(__name__)

# Variable globale pour stocker le statut
transcription_status = {}


def detect_platform(url):
    """Détecte la plateforme depuis l'URL"""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'tiktok.com' in url:
        return 'tiktok'
    return None


def extract_video_id(url):
    """Extrait l'ID de la vidéo YouTube depuis l'URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url


def get_youtube_transcript(video_url, language):
    """Récupère la transcription d'une vidéo YouTube"""
    try:
        video_id = extract_video_id(video_url)
        ytt_api = YouTubeTranscriptApi()
        
        if language == "auto":
            fetched = ytt_api.fetch(video_id)
        else:
            try:
                fetched = ytt_api.fetch(video_id, languages=[language])
            except:
                fetched = ytt_api.fetch(video_id)
        
        full_text = '\n'.join([snippet.text for snippet in fetched])
        return full_text, None
    
    except Exception as e:
        return None, str(e)


def get_tiktok_transcript(video_url, language, task_id):
    """Récupère la transcription d'une vidéo TikTok via Whisper"""
    try:
        import yt_dlp
        import whisper
        
        transcription_status[task_id] = "Téléchargement de la vidéo..."
        
        # Créer un dossier temporaire
        temp_dir = tempfile.mkdtemp()
        audio_file = os.path.join(temp_dir, "audio")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': audio_file + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=True)
        
        # Le fichier final sera audio.mp3
        final_audio = audio_file + '.mp3'
        
        # Vérifier que le fichier existe
        if not os.path.exists(final_audio):
            for file in os.listdir(temp_dir):
                if file.startswith('audio'):
                    final_audio = os.path.join(temp_dir, file)
                    break
        
        if not os.path.exists(final_audio):
            transcription_status[task_id] = "error"
            return None, "Impossible de télécharger l'audio de la vidéo"
        
        transcription_status[task_id] = "Transcription en cours..."
        
        model_size = "base"
        model = whisper.load_model(model_size)
        
        whisper_lang = None if language == "auto" else language
        result = model.transcribe(final_audio, language=whisper_lang)
        
        # Nettoyer les fichiers temporaires
        try:
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        except:
            pass
        
        transcription_status[task_id] = "completed"
        return result["text"], None
    
    except Exception as e:
        transcription_status[task_id] = "error"
        return None, f"Erreur TikTok: {str(e)}"


@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Endpoint pour transcrire une vidéo"""
    data = request.json
    url = data.get('url', '').strip()
    language = data.get('language', 'auto')
    platform = data.get('platform', 'auto')
    
    if not url:
        return jsonify({'error': 'URL manquante'}), 400
    
    # Détecter la plateforme
    if platform == 'auto':
        platform = detect_platform(url)
        if not platform:
            return jsonify({'error': 'Impossible de détecter la plateforme'}), 400
    
    if platform == 'youtube':
        transcript, error = get_youtube_transcript(url, language)
        if error:
            return jsonify({'error': error}), 500
        return jsonify({'transcript': transcript, 'platform': 'youtube'})
    
    elif platform == 'tiktok':
        # Pour TikTok, on retourne un task_id et on traite en arrière-plan
        import uuid
        task_id = str(uuid.uuid4())
        transcription_status[task_id] = "starting"
        
        def process_tiktok():
            transcript, error = get_tiktok_transcript(url, language, task_id)
            if error:
                transcription_status[task_id] = f"error:{error}"
            else:
                transcription_status[task_id] = f"completed:{transcript}"
        
        thread = threading.Thread(target=process_tiktok)
        thread.daemon = True
        thread.start()
        
        return jsonify({'task_id': task_id, 'platform': 'tiktok'})
    
    return jsonify({'error': 'Plateforme non supportée'}), 400


@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """Récupère le statut d'une transcription TikTok"""
    status = transcription_status.get(task_id, 'unknown')
    
    if status.startswith('completed:'):
        transcript = status.replace('completed:', '', 1)
        return jsonify({'status': 'completed', 'transcript': transcript})
    elif status.startswith('error:'):
        error = status.replace('error:', '', 1)
        return jsonify({'status': 'error', 'error': error})
    else:
        return jsonify({'status': 'processing', 'message': status})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
