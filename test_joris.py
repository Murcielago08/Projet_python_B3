import requests
from bs4 import BeautifulSoup
from datetime import date
from notion_client import Client
import re

# 🔐 Config Notion (remplace avec TES infos)
NOTION_TOKEN = "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"
DATABASE_ID = "21e62387b3248010ae86c4b3dc86b5fc"

notion = Client(auth=NOTION_TOKEN)

def scrape_tldr_articles():
    today = date.today().strftime("%Y-%m-%d")
    url = f"https://tldr.tech/data/{today}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"⚠️ Erreur HTTP {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for article in soup.select("article"):
        # Extraction du titre et de la durée de lecture
        title = ""
        reading_time = ""
        h2 = article.find("h2")
        h3 = article.find("h3")
        title_tag = h2 or h3
        if title_tag:
            full_title = title_tag.text.strip()
            match = re.search(r"\(([\d]+ [a-zA-Z ]*read)\)", full_title)
            if match:
                reading_time = match.group(1)
                title = re.sub(r"\s*\([\d]+ [a-zA-Z ]*read\)", "", full_title)
            else:
                title = full_title

        # Extraction de l'URL
        link_tag = None
        if h2 and h2.find("a", href=True):
            link_tag = h2.find("a", href=True)
        elif h3 and h3.find("a", href=True):
            link_tag = h3.find("a", href=True)
        else:
            link_tag = article.find("a", href=True)
        url = link_tag['href'] if link_tag else ""

        # Extraction du résumé
        summary = ""
        summary_tag = article.find(lambda tag: tag.name in ["div", "p"] and tag.get("class") and any("summary" in c or "tldr" in c for c in tag.get("class")))
        if not summary_tag:
            summary_tag = article.find("div", class_="newsletter-html")
        if not summary_tag:
            title_tag = h2 or h3
            if title_tag:
                next_tag = title_tag.find_next_sibling()
                while next_tag and next_tag.name != "p":
                    next_tag = next_tag.find_next_sibling()
                if next_tag and next_tag.name == "p":
                    summary_tag = next_tag
        if not summary_tag:
            for p in article.find_all("p"):
                if p.text.strip():
                    summary_tag = p
                    break
        if summary_tag:
            summary = summary_tag.text.strip()

        articles.append({
            "title": title,
            "url": url,
            "reading_time": reading_time,
            "summary": summary,
            "date": today  # Ajout de la date du jour
        })

    return articles

def save_to_txt(articles, filename="tldr_articles.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for idx, art in enumerate(articles, 1):
            f.write(f"Article {idx}:\n")
            f.write(f"  Titre: {art['title']}\n")
            f.write(f"  URL: {art['url']}\n")
            f.write(f"  Durée de lecture: {art['reading_time']}\n")
            f.write(f"  Résumé: {art['summary']}\n\n")
    print(f"✅ Articles enregistrés dans {filename}")

def send_to_notion(articles):
    for art in articles:
        try:
            notion.pages.create(
                parent={"database_id": DATABASE_ID},
                properties={
                    "Titre": {
                        "title": [{"text": {"content": art["title"] or "Sans titre"}}]
                    },
                    "URL": {"url": art["url"] or "https://tldr.tech"},
                    "Durée de lecture": {
                        "rich_text": [{"text": {"content": art["reading_time"] or "Inconnue"}}]
                    },
                    "Résumé IDLR": {
                        "rich_text": [{"text": {"content": art["summary"] or "Pas de résumé"}}]
                    },
                    "Date de récupération": {  # Nom exact de la colonne date dans Notion
                        "date": {"start": art["date"]}
                    }
                }
            )
            print(f"✅ Envoyé à Notion : {art['title'][:50]}")
        except Exception as e:
            print(f"❌ Erreur en envoyant '{art['title']}': {e}")
            break

# 🔁 Pipeline complet
if __name__ == "__main__":
    print("🔍 Scraping TLDR...")
    articles = scrape_tldr_articles()

    if articles:
        save_to_txt(articles)
        send_to_notion(articles)
    else:
        print("⚠️ Aucun article trouvé ou erreur de scraping.")