-- Création de la base (même si elle est déjà créée via MYSQL_DATABASE pour garantir l'existence)
CREATE DATABASE IF NOT EXISTS crm_ecommerce;
USE crm_ecommerce;

-- Table client
CREATE TABLE IF NOT EXISTS client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL
);

-- Table commande
CREATE TABLE IF NOT EXISTS commande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    montant DECIMAL(10,2) NOT NULL,
    nb_articles INT NOT NULL,
    id_client INT,
    FOREIGN KEY (id_client) REFERENCES client(id)
);

-- Supprimer l'utilisateur s'il existe déjà (important pour éviter les conflits au redémarrage)
DROP USER IF EXISTS 'crm_user'@'%';

-- Créer un utilisateur avec le plugin mysql_native_password (compatible avec DBeaver)
CREATE USER 'crm_user'@'%' IDENTIFIED WITH mysql_native_password BY 'crm_password';

-- Donner les privilèges sur la base
GRANT ALL PRIVILEGES ON crm_ecommerce.* TO 'crm_user'@'%';
FLUSH PRIVILEGES;
