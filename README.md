# YouTube & TikTok Transcription

![Test Status](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Test%20Application/badge.svg)
![Deploy Status](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Deploy%20to%20Docker%20Hub/badge.svg)

Application web pour transcrire des vidéos YouTube et TikTok avec interface graphique moderne.

## 🌟 Fonctionnalités

- ✅ Interface web responsive et moderne
- ✅ Transcription YouTube (sous-titres natifs)
- ✅ Transcription TikTok (via Whisper AI)
- ✅ Détection automatique de la plateforme
- ✅ Support multi-langues (Français, English, Auto)
- ✅ Copie dans le presse-papier
- ✅ Téléchargement en fichier texte
- ✅ Interface desktop (tkinter) également disponible

## 🚀 Déploiement

### Option 1: Docker (Recommandé)

```bash
# Cloner le repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Lancer avec Docker Compose
docker-compose up -d

# Accéder à http://localhost:5000
```

### Option 2: Déploiement local

**Prérequis:** Python 3.8+ et FFmpeg

```bash
# Installer FFmpeg
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application web
python app.py

# Accéder à http://localhost:5000
```

### Option 3: Interface Desktop (GUI)

```bash
pip install -r requirements.txt
python youtube_transcription_gui.py
```

## 🐳 Docker Hub

L'image Docker est automatiquement construite et publiée sur Docker Hub via GitHub Actions.

```bash
docker pull YOUR_DOCKERHUB_USERNAME/video-transcription:latest
docker run -p 5000:5000 YOUR_DOCKERHUB_USERNAME/video-transcription:latest
```

## 📝 Configuration GitHub Actions

Pour activer le déploiement automatique sur Docker Hub:

1. Créez un compte sur [Docker Hub](https://hub.docker.com)
2. Créez un Access Token dans Docker Hub (Account Settings > Security)
3. Ajoutez ces secrets dans votre repo GitHub (Settings > Secrets):
   - `DOCKERHUB_USERNAME`: votre nom d'utilisateur Docker Hub
   - `DOCKERHUB_TOKEN`: votre access token Docker Hub

## 🌐 Déploiement sur le Cloud

### Heroku
```bash
heroku create your-app-name
heroku container:push web
heroku container:release web
```

### Railway / Render
Connectez simplement votre repo GitHub et ces plateformes détecteront automatiquement le Dockerfile.

## 📦 Structure du Projet

```
.
├── app.py                          # Application Flask (web)
├── youtube_transcription_gui.py    # Interface desktop (tkinter)
├── youtube_transcription.py        # Script CLI
├── templates/
│   └── index.html                  # Interface web
├── requirements.txt                # Dépendances Python
├── Dockerfile                      # Configuration Docker
├── docker-compose.yml              # Docker Compose
└── .github/workflows/
    ├── test.yml                    # Tests automatiques
    ├── release.yml                 # Releases GitHub
    └── deploy.yml                  # Déploiement Docker Hub
```

## 🛠️ Technologies

- **Backend**: Flask, Python
- **Transcription**: youtube-transcript-api, Whisper AI, yt-dlp
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Déploiement**: Docker, GitHub Actions

## 📄 Licence

MIT

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
