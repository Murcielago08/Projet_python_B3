import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

def create_database(name, properties):
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
    response = notion.databases.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        title=[{"type": "text", "text": {"content": name}}],
        properties=properties,
    )
    print(f"{name} créé : {response['id']}")
    return response["id"]

if __name__ == "__main__":
    kb_props = {
        "catégorie": {"select": {}},
        "réponse_générique": {"rich_text": {}}
    }
    kb_id = create_database("Réponses support", kb_props)

    contact_props = {
        "email_client": {"email": {}},
        "nom_prenom": {"title": {}},
        "id_commande": {"rich_text": {}},
        "message_initial": {"rich_text": {}},
        "catégorie": {"select": {}},
        "réponse_personnalisée": {"rich_text": {}},
        "statut": {"select": {}}
    }
    contacts_id = create_database("Contacts clients", contact_props)

    with open(".env", "a") as f:
        f.write(f"\nNOTION_KB_DB_ID={kb_id}")
        f.write(f"\nNOTION_CONTACTS_DB_ID={contacts_id}")
