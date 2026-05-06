# YouTube & TikTok Transcription

![Deploy to GitHub Pages](https://github.com/ClaudelMbz/transcriptor/workflows/Deploy%20to%20GitHub%20Pages/badge.svg)

Application web pour transcrire des vidéos YouTube et TikTok.

## 🌐 Demo Live

**Interface Web:** [https://claudelmbz.github.io/transcriptor/](https://claudelmbz.github.io/transcriptor/)

## 🚀 Déploiement en 2 Étapes

### Étape 1: Interface Web (GitHub Pages) ✅ DÉJÀ FAIT

L'interface est automatiquement déployée sur GitHub Pages à chaque push.

### Étape 2: Backend API (Gratuit sur Render)

Pour que la transcription fonctionne, déployez le backend:

1. **Créez un compte sur [Render.com](https://render.com)** (gratuit)
2. **Cliquez "New +" → "Web Service"**
3. **Connectez ce repo GitHub**
4. **Render détecte automatiquement `render.yaml`**
5. **Cliquez "Create Web Service"**
6. **Copiez l'URL de votre service** (ex: `https://your-app.onrender.com`)
7. **Collez cette URL dans l'interface web** quand vous l'utilisez

C'est tout ! 🎉

## 📖 Comment Utiliser

1. Allez sur [https://claudelmbz.github.io/transcriptor/](https://claudelmbz.github.io/transcriptor/)
2. Déployez le backend sur Render (une seule fois)
3. Collez l'URL du backend dans l'interface
4. Collez une URL YouTube ou TikTok
5. Cliquez "Transcrire"
6. ✅ Votre transcription apparaît !

## 🌟 Fonctionnalités

- ✅ Interface web moderne et responsive
- ✅ Déployée sur GitHub Pages (comme xVisuals)
- ✅ Transcription YouTube
- ✅ Transcription TikTok (via Whisper AI)
- ✅ Détection automatique de la plateforme
- ✅ Support multi-langues (Français, English, Auto)
- ✅ Copie dans le presse-papier
- ✅ Téléchargement en fichier texte
- ✅ Sauvegarde de l'URL backend (localStorage)

## 🛠️ Architecture

```
┌─────────────────────┐
│  GitHub Pages       │  ← Interface Web (index.html)
│  (Frontend)         │     Déployée automatiquement
└──────────┬──────────┘
           │
           │ API Calls
           ▼
┌─────────────────────┐
│  Render.com         │  ← Backend Python (app.py)
│  (Backend API)      │     Déployé manuellement (1 fois)
└─────────────────────┘
```

## 📦 Fichiers Principaux

- `index.html` - Interface web complète (déployée sur GitHub Pages)
- `app.py` - Backend Flask (à déployer sur Render)
- `render.yaml` - Configuration Render
- `.github/workflows/deploy-pages.yml` - Auto-déploiement GitHub Pages

## 🔧 Installation Locale (Optionnel)

```bash
# Installer FFmpeg
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg

# Installer les dépendances
pip install -r requirements.txt

# Lancer le backend
python app.py

# Ouvrir index.html dans un navigateur
# Entrer http://localhost:5000 comme URL backend
```

## 🎯 Alternatives de Déploiement Backend

Si vous ne voulez pas utiliser Render:

### Railway.app
1. [railway.app](https://railway.app) → "New Project"
2. Connectez votre repo
3. ✅ Déployé automatiquement

### Vercel (YouTube uniquement)
1. [vercel.com](https://vercel.com) → "New Project"
2. Importez votre repo
3. ✅ Déployé instantanément

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

## 🖥️ Interface Desktop (Bonus)

Si vous préférez une application desktop:

```bash
pip install -r requirements.txt
python youtube_transcription_gui.py
```

## 🛠️ Technologies

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Flask, Python
- **Transcription**: youtube-transcript-api, Whisper AI, yt-dlp
- **Déploiement**: GitHub Pages + Render/Railway

## 📝 Configuration GitHub Pages

Pour activer GitHub Pages sur votre fork:

1. Settings → Pages
2. Source: **GitHub Actions**
3. L'interface sera disponible sur: `https://YOUR_USERNAME.github.io/transcriptor/`

## 📄 Licence

MIT

---

Made with ❤️ by [Claudel](https://github.com/ClaudelMbz)
