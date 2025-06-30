from gtts import gTTS
import os
import re

def text_to_speech(text, filepath, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filepath)
        print(f"🎧 Audio généré : {filepath}")
    except Exception as e:
        print(f"[ERREUR AUDIO] {e}")

def sanitize_filename(title):
    # Remplace espaces par _ et enlève les caractères non alphanumériques/_/-
    filename = re.sub(r'\s+', '_', title)
    filename = re.sub(r'[^\w\-]', '', filename)
    return filename

def generate_audio_for_articles(articles):
    if not articles:
        return
    # Si plusieurs thèmes, on génère un dossier par thème
    theme_date_folders = {}
    for i, article in enumerate(articles, 1):
        theme = article.get("theme", "theme")
        date_str = article.get("date", "date")
        folder = f"audios_articles_{theme}_{date_str}"
        if folder not in theme_date_folders:
            os.makedirs(folder, exist_ok=True)
            theme_date_folders[folder] = True
        title = article.get("title", "No title")
        summary = article.get("resume_ia", "No summary available due to AI error.")
        safe_title = sanitize_filename(title)
        filename = f"{safe_title}.mp3"
        filepath = os.path.join(folder, filename)
        text = f"Article {i}: {title}. Summary: {summary}"
        text_to_speech(text, filepath, lang="en")
        article["audio_path"] = filepath  # On stocke le chemin du fichier audio

def delete_local_audios(articles):
    folders = set()
    for article in articles:
        path = article.get("audio_path")
        if path and os.path.exists(path):
            os.remove(path)
            print(f"🗑️ Fichier supprimé : {path}")
            folder = os.path.dirname(path)
            folders.add(folder)
    # Supprime chaque dossier s'il est vide
    for folder in folders:
        if folder and os.path.isdir(folder) and not os.listdir(folder):
            os.rmdir(folder)
