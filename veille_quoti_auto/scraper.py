import requests
from bs4 import BeautifulSoup
from datetime import date
import re

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
        url = link_tag['href'] if link_tag else ""

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
            "date": today
        })

    return articles
