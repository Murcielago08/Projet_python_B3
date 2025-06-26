import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def enrich_with_ai(articles):
    enriched_articles = []

    for art in articles:
        prompt = (
            f"Catégorise cet article en un seul mot clé pertinent et fais un résumé court:\n\n"
            f"Titre: {art['title']}\n"
            f"Résumé: {art['summary']}\n\n"
            f"Réponds au format JSON:\n"
            f'{{"categorie": "...", "resume": "..."}}'
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7,
            )
            content = response.choices[0].message.content

            import json
            data = json.loads(content)

            art["categorie_ia"] = data.get("categorie", "Erreur IA: catégorie manquante")
            art["resume_ia"] = data.get("resume", "Erreur IA: résumé manquant")

            print(f"✨ Enrichissement IA : {art['title'][:50]}...")

        except Exception as e:
            erreur_msg = f"Erreur IA: {str(e)}"
            print(f"❌ {erreur_msg}")
            art["categorie_ia"] = erreur_msg
            art["resume_ia"] = erreur_msg

        enriched_articles.append(art)

    return enriched_articles
