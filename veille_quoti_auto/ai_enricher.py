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

def generate_categorie(article):
    prompt = f"""Donne les catégories principales de l'article suivant en français (exemple: Technologie, Santé, Politique, etc).
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
        # On prend juste le premier mot retourné
        return response["message"]["content"].strip().split()[0]
    except Exception as e:
        print(f"❌ Erreur IA locale (catégorie) : {e}")
        return "Autre"

def enrich_article_with_ai(article, theme=None):
    article["resume_ia"] = generate_resume(article)
    # Si un thème est choisi, on le met en catégorie, sinon IA
    if theme and theme != "all":
        article["categorie_ia"] = theme.capitalize()
    else:
        article["categorie_ia"] = generate_categorie(article)
    return article

def enrich_with_ai(articles, theme=None):
    return [enrich_article_with_ai(article, theme=theme) for article in articles]
