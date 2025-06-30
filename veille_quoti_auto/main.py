import os
from scraper import scrape_tldr_articles, ask_theme
from ai_enricher import enrich_with_ai
from audio_generator import generate_audio_for_articles, delete_local_audios
from notion_push import send_to_notion
from dotenv import load_dotenv

def main():
    load_dotenv()

    theme = ask_theme()
    print(f"--- Thème en cours d'exécution : {theme} ---")
    print("🔍 Scraping en cours...")
    articles = scrape_tldr_articles(theme=theme)

    if not articles:
        print("⚠️ Aucun article trouvé.")
        return

    print("✨ Enrichissement IA en cours...")
    articles = enrich_with_ai(articles, theme=theme)
    
    if not articles:
        print("❌ Aucun article à traiter.")
        return

    print("🔊 Génération audio...")
    generate_audio_for_articles(articles)

    print("📨 Envoi vers Notion...")
    send_to_notion(articles, theme=theme)

    # print("🧹 Nettoyage fichiers audio locaux...")
    # delete_local_audios(articles)

if __name__ == "__main__":
    main()
