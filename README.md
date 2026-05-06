# YouTube & TikTok Transcription

![Test Status](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Test%20Application/badge.svg)

Application web pour transcrire des vidéos YouTube et TikTok.

## 🚀 Déploiement Rapide (Sans Docker)

### Option 1: Render.com (Recommandé - Gratuit)

1. Créez un compte sur [Render.com](https://render.com)
2. Cliquez sur "New +" → "Web Service"
3. Connectez votre repo GitHub
4. Render détectera automatiquement le `render.yaml`
5. Cliquez sur "Create Web Service"
6. ✅ Votre app sera déployée automatiquement !

**Configuration automatique via GitHub Actions:**
- Allez dans Render Dashboard → Settings → Deploy Hook
- Copiez l'URL du Deploy Hook
- Dans GitHub: Settings → Secrets → New secret
  - Name: `RENDER_DEPLOY_HOOK_URL`
  - Value: [votre deploy hook URL]
- Chaque push déclenchera un redéploiement automatique

### Option 2: Railway.app (Gratuit)

1. Créez un compte sur [Railway.app](https://railway.app)
2. Cliquez sur "New Project" → "Deploy from GitHub repo"
3. Sélectionnez votre repo
4. Railway détectera automatiquement la configuration
5. ✅ Déployé en quelques secondes !

### Option 3: Vercel (Gratuit)

1. Créez un compte sur [Vercel.com](https://vercel.com)
2. Cliquez sur "Add New" → "Project"
3. Importez votre repo GitHub
4. Vercel détectera le `vercel.json`
5. ✅ Déployé instantanément !

**Note:** Vercel a des limitations pour les fonctions serverless (temps d'exécution limité). Préférez Render ou Railway pour TikTok.

### Option 4: Heroku (Gratuit avec limitations)

```bash
# Installer Heroku CLI
# Puis:
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

### Option 5: GitHub Pages (Interface statique uniquement)

L'interface HTML sera déployée automatiquement sur GitHub Pages, mais sans backend (YouTube/TikTok ne fonctionneront pas).

Pour activer:
1. Settings → Pages
2. Source: GitHub Actions
3. L'interface sera disponible sur: `https://YOUR_USERNAME.github.io/YOUR_REPO`

## 📦 Fichiers de Configuration

- `render.yaml` - Configuration Render
- `railway.json` - Configuration Railway  
- `vercel.json` - Configuration Vercel
- `Procfile` - Configuration Heroku
- `runtime.txt` - Version Python
- `.github/workflows/deploy-render.yml` - Auto-déploiement Render
- `.github/workflows/deploy-pages.yml` - Déploiement GitHub Pages

## 🛠️ Installation Locale

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

## 🌟 Fonctionnalités

- ✅ Interface web responsive et moderne
- ✅ Transcription YouTube (sous-titres natifs)
- ✅ Transcription TikTok (via Whisper AI)
- ✅ Détection automatique de la plateforme
- ✅ Support multi-langues (Français, English, Auto)
- ✅ Copie dans le presse-papier
- ✅ Téléchargement en fichier texte
- ✅ Interface desktop (tkinter) également disponible

## 🖥️ Interface Desktop (GUI)

```bash
pip install -r requirements.txt
python youtube_transcription_gui.py
```

## 🛠️ Technologies

- **Backend**: Flask, Python
- **Transcription**: youtube-transcript-api, Whisper AI, yt-dlp
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Déploiement**: Render, Railway, Vercel, Heroku, GitHub Actions

## 📝 Variables d'Environnement (Optionnel)

Aucune variable d'environnement n'est requise pour le fonctionnement de base.

## 🎯 Comparaison des Plateformes

| Plateforme | Gratuit | Auto-deploy | TikTok Support | Setup |
|------------|---------|-------------|----------------|-------|
| **Render** | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **Railway** | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **Vercel** | ✅ | ✅ | ⚠️ Limité | ⭐⭐⭐⭐ |
| **Heroku** | ⚠️ Limité | ✅ | ✅ | ⭐⭐⭐ |
| **GitHub Pages** | ✅ | ✅ | ❌ | ⭐⭐⭐⭐⭐ |

**Recommandation:** Utilisez **Render.com** ou **Railway.app** pour la meilleure expérience gratuite.

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
