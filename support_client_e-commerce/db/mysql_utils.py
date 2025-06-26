import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='crm_user',
        password='crm_password',
        database='crm_ecommerce'
    )

def find_client_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM client WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def find_commandes_by_client_id(client_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM commande WHERE id_client = %s", (client_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
