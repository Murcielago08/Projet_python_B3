import os
from notion_client import Client

notion = Client(auth=os.getenv("NOTION_TOKEN"))

def get_reponse_generique(categorie):
    db_id = os.getenv("NOTION_KB_DB_ID")
    query = notion.databases.query(database_id=db_id, filter={
        "property": "catégorie",
        "select": {"equals": categorie}
    })
    if query['results']:
        return query['results'][0]['properties']['réponse_générique']['rich_text'][0]['text']['content']
    return None

def enregistrer_contact(data):
    db_id = os.getenv("NOTION_CONTACTS_DB_ID")
    notion.pages.create(
        parent={"database_id": db_id},
        properties=data
    )