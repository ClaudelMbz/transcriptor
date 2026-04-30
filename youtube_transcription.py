#!/usr/bin/env python3
"""
Script pour transcrire des vidéos YouTube
"""

from youtube_transcript_api import YouTubeTranscriptApi
import sys
import re


def extract_video_id(url):
    """Extrait l'ID de la vidéo depuis l'URL YouTube"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url  # Assume it's already a video ID


def get_transcript(video_url, language='fr'):
    """Récupère la transcription d'une vidéo YouTube"""
    try:
        video_id = extract_video_id(video_url)
        ytt_api = YouTubeTranscriptApi()
        
        # Essayer d'abord avec la langue spécifiée
        try:
            fetched = ytt_api.fetch(video_id, languages=[language])
        except:
            # Si pas disponible, prendre la première langue disponible
            fetched = ytt_api.fetch(video_id)
        
        # Formater la transcription
        full_text = '\n'.join([snippet.text for snippet in fetched])
        return full_text
    
    except Exception as e:
        return f"Erreur: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcription.py <URL_YouTube> [langue]")
        print("Exemple: python youtube_transcription.py https://www.youtube.com/watch?v=VIDEO_ID fr")
        sys.exit(1)
    
    url = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else 'fr'
    
    print(f"Récupération de la transcription...\n")
    transcript = get_transcript(url, lang)
    print(transcript)
