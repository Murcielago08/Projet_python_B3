import os
from db.mysql_utils import find_client_by_email, find_commandes_by_client_id
from notion.notion_client import get_reponse_generique, enregistrer_contact
from ai.classifier import classify
from dotenv import load_dotenv

load_dotenv()

def process_support_message(email, message, id_commande=None):
    client = find_client_by_email(email)
    if not client:
        print("Client non trouvé")
        return

    commandes = find_commandes_by_client_id(client['id'])
    categorie = classify(message)
    reponse_gen = get_reponse_generique(categorie)

    if not reponse_gen:
        print("Pas de réponse générique trouvée")
        return

    reponse_perso = f"Bonjour {client['prenom']} {client['nom']},\n\n{reponse_gen}\n\nCommande: {id_commande if id_commande else 'N/A'}"

    enregistrer_contact({
        "email_client": {"email": email},
        "nom_prenom": {"title": [{"text": {"content": f"{client['prenom']} {client['nom']}"}}]},
        "id_commande": {"rich_text": [{"text": {"content": id_commande or "inconnu"}}]},
        "message_initial": {"rich_text": [{"text": {"content": message}}]},
        "catégorie": {"select": {"name": categorie}},
        "réponse_personnalisée": {"rich_text": [{"text": {"content": reponse_perso}}]},
        "statut": {"select": {"name": "Pas commencé"}}
    })

    print("Réponse enregistrée dans Notion")

# Exemple d’appel (à adapter à une route Flask ou un script CLI)
if __name__ == "__main__":
    process_support_message(
        email="client@example.com",
        message="j’ai un souci avec ma livraison",
        id_commande="CMD12345"
    )