# YouTube Transcription

![Test Status](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Test%20Application/badge.svg)

Outil simple pour transcrire des vidéos YouTube avec interface graphique.

## Installation

### Option 1: Télécharger l'exécutable (recommandé)
Téléchargez la dernière version depuis [Releases](https://github.com/YOUR_USERNAME/YOUR_REPO/releases)

### Option 2: Installation depuis le code source

```bash
pip install -r requirements.txt
```

## Utilisation

### Interface graphique (recommandé)

```bash
python youtube_transcription_gui.py
```

L'interface permet de :
- Coller l'URL YouTube
- Choisir la langue (Français, English, Auto)
- Transcrire la vidéo
- Copier le texte dans le presse-papier
- Sauvegarder dans un fichier

### Ligne de commande

```bash
python youtube_transcription.py <URL_YouTube> [langue]
```

### Exemples

```bash
# Transcription en français (par défaut)
python youtube_transcription.py https://www.youtube.com/watch?v=VIDEO_ID

# Transcription en anglais
python youtube_transcription.py https://www.youtube.com/watch?v=VIDEO_ID en
```

## Formats d'URL supportés

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `VIDEO_ID` directement
