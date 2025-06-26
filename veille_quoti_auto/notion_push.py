from notion_client import Client
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


notion = Client(auth=NOTION_TOKEN)

def upload_audio_to_notion(filepath):
    """
    Notion API ne permet pas d’uploader directement un fichier.
    On doit uploader le fichier quelque part (ex: stockage cloud) puis mettre l'URL ici.
    Comme solution simple, on suppose que le fichier est déjà accessible via URL externe.
    Si non, il faut héberger ailleurs ou stocker local (mais pas possible dans Notion).
    """
    # Pour simplifier, on ne gère pas l'upload ici.
    # On retourne None pour dire pas de lien externe.
    return None

def send_to_notion(articles):
    for art in articles:
        try:
            props = {
                "Titre": {
                    "title": [{"text": {"content": art.get("title", "Sans titre")}}]
                },
                "URL": {
                    "url": art.get("url", "https://tldr.tech")
                },
                "Durée de lecture": {
                    "rich_text": [{"text": {"content": art.get("reading_time", "Inconnue")}}]
                },
                "Résumé TLDR": {
                    "rich_text": [{"text": {"content": art.get("summary", "Pas de résumé")}}]
                },
                "Date de récupération": {
                    "date": {"start": art.get("date", date.today().isoformat())}
                },
                "Résumé IA": {
                    "rich_text": [{"text": {"content": art.get("resume_ia", "Non généré")}}]
                },
                # "Catégorie": {
                #     "select": {"name": art.get("categorie_ia", "Autre")}
                # }
            }

            # Gestion de l'audio si on a un lien externe
            audio_url = art.get("audio_url")
            if audio_url:
                props["Audio"] = {
                    "files": [{
                        "name": "Résumé audio",
                        "type": "external",
                        "external": {"url": audio_url}
                    }]
                }

            notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties=props
            )

            print(f"✅ Article ajouté à Notion : {art['title'][:50]}")

        except Exception as e:
            print(f"❌ Erreur avec l'article '{art.get('title')}': {e}")
