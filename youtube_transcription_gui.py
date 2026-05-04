#!/usr/bin/env python3
"""
Interface graphique pour transcrire des vidéos YouTube et TikTok
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from youtube_transcript_api import YouTubeTranscriptApi
import re
import threading
import pyperclip
import os
import tempfile


class VideoTranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Transcription - YouTube & TikTok")
        self.root.geometry("800x650")
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # URL Input
        ttk.Label(main_frame, text="URL (YouTube/TikTok):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Platform detection
        ttk.Label(main_frame, text="Plateforme:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.platform_var = tk.StringVar(value="auto")
        platform_frame = ttk.Frame(main_frame)
        platform_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(platform_frame, text="Auto", variable=self.platform_var, value="auto").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(platform_frame, text="YouTube", variable=self.platform_var, value="youtube").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(platform_frame, text="TikTok", variable=self.platform_var, value="tiktok").pack(side=tk.LEFT, padx=5)
        
        # Langue
        ttk.Label(main_frame, text="Langue:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.lang_var = tk.StringVar(value="fr")
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(lang_frame, text="Français", variable=self.lang_var, value="fr").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(lang_frame, text="English", variable=self.lang_var, value="en").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(lang_frame, text="Auto", variable=self.lang_var, value="auto").pack(side=tk.LEFT, padx=5)
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.transcribe_btn = ttk.Button(button_frame, text="Transcrire", command=self.start_transcription)
        self.transcribe_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Copier", command=self.copy_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Effacer", command=self.clear_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sauvegarder", command=self.save_text).pack(side=tk.LEFT, padx=5)
        
        # Zone de texte pour la transcription
        ttk.Label(main_frame, text="Transcription:").grid(row=4, column=0, sticky=(tk.W, tk.N), pady=5)
        
        self.text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=20)
        self.text_area.grid(row=4, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        # Barre de statut
        self.status_var = tk.StringVar(value="Prêt")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def detect_platform(self, url):
        """Détecte la plateforme depuis l'URL"""
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'tiktok.com' in url:
            return 'tiktok'
        return None
    
    def extract_video_id(self, url):
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
    
    def get_youtube_transcript(self, video_url, language):
        """Récupère la transcription d'une vidéo YouTube"""
        try:
            video_id = self.extract_video_id(video_url)
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
    
    def get_tiktok_transcript(self, video_url, language):
        """Récupère la transcription d'une vidéo TikTok via Whisper"""
        try:
            import yt_dlp
            import whisper
            
            # Créer un dossier temporaire
            temp_dir = tempfile.mkdtemp()
            audio_file = os.path.join(temp_dir, "audio")
            
            # Télécharger l'audio avec yt-dlp
            self.root.after(0, lambda: self.status_var.set("Téléchargement de la vidéo..."))
            
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
                info = ydl.extract_info(video_url, download=True)
            
            # Le fichier final sera audio.mp3
            final_audio = audio_file + '.mp3'
            
            # Vérifier que le fichier existe
            if not os.path.exists(final_audio):
                # Chercher le fichier avec n'importe quelle extension
                for file in os.listdir(temp_dir):
                    if file.startswith('audio'):
                        final_audio = os.path.join(temp_dir, file)
                        break
            
            if not os.path.exists(final_audio):
                return None, "Impossible de télécharger l'audio de la vidéo"
            
            # Transcrire avec Whisper
            self.root.after(0, lambda: self.status_var.set("Transcription en cours (cela peut prendre du temps)..."))
            
            model_size = "base"  # Options: tiny, base, small, medium, large
            model = whisper.load_model(model_size)
            
            # Déterminer la langue pour Whisper
            whisper_lang = None if language == "auto" else language
            
            result = model.transcribe(final_audio, language=whisper_lang)
            
            # Nettoyer les fichiers temporaires
            try:
                for file in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, file))
                os.rmdir(temp_dir)
            except:
                pass
            
            return result["text"], None
        
        except Exception as e:
            return None, f"Erreur TikTok: {str(e)}"
    
    def get_transcript(self, video_url, language, platform):
        """Récupère la transcription selon la plateforme"""
        # Détecter la plateforme si auto
        if platform == "auto":
            platform = self.detect_platform(video_url)
            if not platform:
                return None, "Impossible de détecter la plateforme. Veuillez la sélectionner manuellement."
        
        if platform == "youtube":
            return self.get_youtube_transcript(video_url, language)
        elif platform == "tiktok":
            return self.get_tiktok_transcript(video_url, language)
        else:
            return None, "Plateforme non supportée"
    
    def start_transcription(self):
        """Lance la transcription dans un thread séparé"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Attention", "Veuillez entrer une URL")
            return
        
        self.transcribe_btn.config(state=tk.DISABLED)
        self.status_var.set("Transcription en cours...")
        self.text_area.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.transcribe_video, args=(url,))
        thread.daemon = True
        thread.start()
    
    def transcribe_video(self, url):
        """Effectue la transcription"""
        language = self.lang_var.get()
        platform = self.platform_var.get()
        transcript, error = self.get_transcript(url, language, platform)
        
        self.root.after(0, self.update_ui, transcript, error)
    
    def update_ui(self, transcript, error):
        """Met à jour l'interface avec le résultat"""
        if error:
            self.text_area.insert(1.0, f"Erreur: {error}")
            self.status_var.set("Erreur lors de la transcription")
            messagebox.showerror("Erreur", f"Impossible de transcrire la vidéo:\n{error}")
        else:
            self.text_area.insert(1.0, transcript)
            self.status_var.set("Transcription terminée")
        
        self.transcribe_btn.config(state=tk.NORMAL)
    
    def copy_text(self):
        """Copie le texte dans le presse-papier"""
        text = self.text_area.get(1.0, tk.END).strip()
        if text:
            pyperclip.copy(text)
            self.status_var.set("Texte copié dans le presse-papier")
        else:
            messagebox.showinfo("Info", "Aucun texte à copier")
    
    def clear_text(self):
        """Efface le texte"""
        self.text_area.delete(1.0, tk.END)
        self.status_var.set("Texte effacé")
    
    def save_text(self):
        """Sauvegarde le texte dans un fichier"""
        from tkinter import filedialog
        
        text = self.text_area.get(1.0, tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "Aucun texte à sauvegarder")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.status_var.set(f"Sauvegardé: {filename}")
                messagebox.showinfo("Succès", "Fichier sauvegardé avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoTranscriptionApp(root)
    root.mainloop()
