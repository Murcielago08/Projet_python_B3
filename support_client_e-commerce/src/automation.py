import mysql.connector
from datetime import datetime

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="crm_ecommerce"
)
cursor = cnx.cursor(dictionary=True)

reponses_support = {
    "livraison": "Bonjour, votre commande est en cours de livraison et vous sera livrée sous 3 à 5 jours ouvrés.",
    "remboursement": "Bonjour, votre demande de remboursement est en cours de traitement. Nous reviendrons vers vous sous 48h.",
    "probleme_produit": "Bonjour, nous sommes désolés pour le problème rencontré. Veuillez nous fournir plus de détails afin de résoudre cela rapidement."
}

def categoriser_demande(message):
    msg = message.lower()
    if "retard" in msg or "livraison" in msg:
        return "livraison"
    elif "remboursement" in msg or "rembourser" in msg:
        return "remboursement"
    elif "problème" in msg or "cassé" in msg or "défectueux" in msg:
        return "probleme_produit"
    else:
        return "autre"

def gerer_ticket(email_client, message, id_commande=None):
    cursor.execute("SELECT * FROM client WHERE email=%s", (email_client,))
    client = cursor.fetchone()
    
    if not client:
        print("Client non trouvé.")
        nom_prenom = "Client inconnu"
        commandes = []
    else:
        nom_prenom = f"{client['prenom']} {client['nom']}"
        cursor.execute("SELECT * FROM commande WHERE id_client=%s", (client['id'],))
        commandes = cursor.fetchall()
    commande_info = None
    if id_commande:
        for c in commandes:
            if c['id'] == id_commande:
                commande_info = c
                break
    categorie = categoriser_demande(message)
    reponse_gen = reponses_support.get(categorie, "Merci pour votre message, nous reviendrons vers vous rapidement.")
    if client and commande_info:
        reponse_perso = (f"Bonjour {client['prenom']}, votre commande #{commande_info['id']} passée le {commande_info['date']} "
                         f"d'un montant de {commande_info['montant']}€ est en traitement.\n\n{reponse_gen}")
    elif client:
        reponse_perso = f"Bonjour {client['prenom']}, {reponse_gen}"
    else:
        reponse_perso = reponse_gen

    ticket = {
        "email_client": email_client,
        "nom_prenom": nom_prenom,
        "id_commande": id_commande,
        "message_initial": message,
        "categorie": categorie,
        "reponse_personnalisee": reponse_perso,
        "statut": "Pas commencé"
    }
    
    print("Ticket créé :", ticket)
    return ticket
if __name__ == "__main__":
    ticket = gerer_ticket(
        email_client="client@example.com",
        message="Bonjour, ma livraison est en retard, que faire ?",
        id_commande=1
    )
