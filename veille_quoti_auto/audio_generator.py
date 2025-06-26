from gtts import gTTS
import os

def text_to_speech(text, filepath, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filepath)
        print(f"🎧 Audio généré : {filepath}")
    except Exception as e:
        print(f"[ERREUR AUDIO] {e}")

def generate_audio_for_articles(articles):
    for i, article in enumerate(articles, 1):
        filename = f"article_{i}.mp3"
        text = f"Article {i}: {article['title']}. Summary: {article['resume_ia']}"
        text_to_speech(text, filename, lang="en")
        article["audio_path"] = filename  # On stocke le chemin du fichier audio

def delete_local_audios(articles):
    for article in articles:
        path = article.get("audio_path")
        if path and os.path.exists(path):
            os.remove(path)
            print(f"🗑️ Fichier supprimé : {path}")
