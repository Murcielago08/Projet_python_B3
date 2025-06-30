import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

def ask_theme():
    themes = [
        "webdev", "infosec", "product", "devops", "founders",
        "design", "marketing", "crypto", "fintech", "data"
    ]
    print("Choisissez un thème parmi la liste suivante ou tapez 'all' pour tout :")
    print(", ".join(themes))
    while True:
        theme = input("Thème (all/tout/" + "/".join(themes) + ") : ").strip().lower()
        if theme in ["all", "tout", ""]:
            return "all"
        if theme in themes:
            return theme
        print("⚠️ Thème invalide. Veuillez choisir dans la liste ou 'all'.")

def get_user_date():
    while True:
        user_input = input("Entrez une date antérieure au format AAAA-MM-JJ (laisser vide pour aujourd'hui) : ")
        if not user_input.strip():
            # Pas de saisie, utiliser la date du jour
            return date.today().strftime("%Y-%m-%d")
        try:
            user_date = datetime.strptime(user_input, "%Y-%m-%d").date()
            return user_date.strftime("%Y-%m-%d")
        except ValueError:
            print("⚠️ Format de date invalide. Veuillez réessayer.")

def scrape_tldr_articles(theme=None):
    themes_list = [
        "webdev", "infosec", "product", "devops", "founders",
        "design", "marketing", "crypto", "fintech", "data"
    ]
    today = get_user_date()
    articles = []

    if theme == "all":
        for th in themes_list:
            url = f"https://tldr.tech/{th}/{today}"
            print(f"🌐 URL utilisée : {url}")
            try:
                response = requests.get(url)
            except requests.RequestException as e:
                print(f"⚠️ Erreur de connexion : {e}")
                continue

            if response.status_code != 200:
                print(f"⚠️ Erreur HTTP {response.status_code} ou pas d'articles pour cette date/thème {th}.")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            for article in soup.select("article"):
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

                link_tag = None
                if h2 and h2.find("a", href=True):
                    link_tag = h2.find("a", href=True)
                elif h3 and h3.find("a", href=True):
                    link_tag = h3.find("a", href=True)
                else:
                    link_tag = article.find("a", href=True)
                url_article = link_tag['href'] if link_tag else ""

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
                    "url": url_article,
                    "reading_time": reading_time,
                    "summary": summary,
                    "date": today,
                    "theme": th
                })
    else:
        if not theme:
            theme = "webdev"
        url = f"https://tldr.tech/{theme}/{today}"
        print(f"🌐 URL utilisée : {url}")
        try:
            response = requests.get(url)
        except requests.RequestException as e:
            print(f"⚠️ Erreur de connexion : {e}")
            return []

        if response.status_code != 200:
            print(f"⚠️ Erreur HTTP {response.status_code} ou pas d'articles pour cette date/thème.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.select("article"):
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

            link_tag = None
            if h2 and h2.find("a", href=True):
                link_tag = h2.find("a", href=True)
            elif h3 and h3.find("a", href=True):
                link_tag = h3.find("a", href=True)
            else:
                link_tag = article.find("a", href=True)
            url_article = link_tag['href'] if link_tag else ""

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
                "url": url_article,
                "reading_time": reading_time,
                "summary": summary,
                "date": today,
                "theme": theme
            })

    return articles if articles else []
