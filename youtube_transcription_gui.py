#!/usr/bin/env python3
"""
Interface graphique pour transcrire des vidéos YouTube
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from youtube_transcript_api import YouTubeTranscriptApi
import re
import threading
import pyperclip


class YouTubeTranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Transcription")
        self.root.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # URL Input
        ttk.Label(main_frame, text="URL YouTube:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Langue
        ttk.Label(main_frame, text="Langue:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.lang_var = tk.StringVar(value="fr")
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(lang_frame, text="Français", variable=self.lang_var, value="fr").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(lang_frame, text="English", variable=self.lang_var, value="en").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(lang_frame, text="Auto", variable=self.lang_var, value="auto").pack(side=tk.LEFT, padx=5)
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.transcribe_btn = ttk.Button(button_frame, text="Transcrire", command=self.start_transcription)
        self.transcribe_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Copier", command=self.copy_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Effacer", command=self.clear_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sauvegarder", command=self.save_text).pack(side=tk.LEFT, padx=5)
        
        # Zone de texte pour la transcription
        ttk.Label(main_frame, text="Transcription:").grid(row=3, column=0, sticky=(tk.W, tk.N), pady=5)
        
        self.text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=20)
        self.text_area.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        # Barre de statut
        self.status_var = tk.StringVar(value="Prêt")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def extract_video_id(self, url):
        """Extrait l'ID de la vidéo depuis l'URL YouTube"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return url
    
    def get_transcript(self, video_url, language):
        """Récupère la transcription d'une vidéo YouTube"""
        try:
            video_id = self.extract_video_id(video_url)
            ytt_api = YouTubeTranscriptApi()
            
            if language == "auto":
                # Laisser l'API choisir la langue par défaut
                fetched = ytt_api.fetch(video_id)
            else:
                # Essayer avec la langue spécifiée
                try:
                    fetched = ytt_api.fetch(video_id, languages=[language])
                except:
                    # Si pas disponible, prendre la première disponible
                    fetched = ytt_api.fetch(video_id)
            
            # Extraire le texte de chaque snippet
            full_text = '\n'.join([snippet.text for snippet in fetched])
            return full_text, None
        
        except Exception as e:
            return None, str(e)
    
    def start_transcription(self):
        """Lance la transcription dans un thread séparé"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Attention", "Veuillez entrer une URL YouTube")
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
        transcript, error = self.get_transcript(url, language)
        
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
    app = YouTubeTranscriptionApp(root)
    root.mainloop()
