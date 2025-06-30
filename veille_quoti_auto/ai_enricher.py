from ollama import Client

client = Client()

def generate_resume(article):
    prompt = f"""Résume l'article suivant en 10 mots max en français (juste le résumé, pas d'introduction ni de conclusion, pas de répétition, pas de phrases incomplètes, pas de fautes d'orthographe).
Titre : {article['title']}
Résumé original : {article['summary']}
URL : {article['url']}
"""
    try:
        response = client.chat(
            model='gemma3:latest',
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"❌ Erreur IA locale (résumé) : {e}")
        return article["summary"]

def generate_categories(article):
    prompt = f"""Donne les catégories principales de l'article suivant en français, séparées par une virgule (exemple: Technologie, Santé, Politique, etc).
Titre : {article['title']}
Résumé original : {article['summary']}
URL : {article['url']}
Réponds uniquement par la liste de catégories, séparées par une virgule.
"""
    try:
        response = client.chat(
            model='gemma3:latest',
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # Découpe la réponse sur les virgules, nettoie les espaces
        raw = response["message"]["content"].strip()
        categories = [c.strip() for c in raw.split(",") if c.strip()]
        return categories if categories else ["Autre"]
    except Exception as e:
        print(f"❌ Erreur IA locale (catégorie) : {e}")
        return ["Autre"]

def enrich_article_with_ai(article, theme=None):
    article["resume_ia"] = generate_resume(article)
    categories_ia = generate_categories(article)
    # print(f"[IA Catégories] {article.get('title', '')[:50]} => {categories_ia}")
    article["categories_ia"] = categories_ia
    # Pour compatibilité Notion, on garde la première catégorie dans 'categorie_ia'
    if theme and theme != "all":
        article["categorie_ia"] = theme.capitalize()
    else:
        article["categorie_ia"] = categories_ia[0] if categories_ia else "Autre"
    return article

def enrich_with_ai(articles, theme=None):
    return [enrich_article_with_ai(article, theme=theme) for article in articles]
