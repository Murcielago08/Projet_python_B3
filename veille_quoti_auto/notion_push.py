from notion_client import Client
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


notion = Client(auth=NOTION_TOKEN)

def upload_audio_to_notion(filepath):
    return None

def send_to_notion(articles, theme=None):
    for art in articles:
        try:
            # Ajoute le thème + toutes les catégories IA (sans doublon)
            categories = []
            theme_val = art.get("theme")
            if theme_val:
                categories.append(str(theme_val).capitalize())
            if art.get("categories_ia"):
                for c in art["categories_ia"]:
                    c_cap = str(c).capitalize()
                    if c_cap not in categories:
                        categories.append(c_cap)
            else:
                cat_ia = art.get("categorie_ia")
                if cat_ia:
                    cat_ia_cap = str(cat_ia).capitalize()
                    if cat_ia_cap not in categories:
                        categories.append(cat_ia_cap)
            if not categories:
                categories = ["Autre"]

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
                    "date": {"start": art["date"]}
                },
                "Résumé IA": {
                    "rich_text": [{"text": {"content": art.get("resume_ia", "Non généré")}}]
                },
                "Catégorie": {
                    "multi_select": [{"name": c} for c in categories]
                }
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
