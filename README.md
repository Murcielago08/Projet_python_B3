# Projet_python_B3

## Sommaire

- [Projet\_python\_B3](#projet_python_b3)
  - [Sommaire](#sommaire)
  - [Récupérer l'env](#récupérer-lenv)
  - [Automatisation du support client e-commerce](#automatisation-du-support-client-e-commerce)
  - [Cas pratique - Automatisation d'une veille quotidienne](#cas-pratique---automatisation-dune-veille-quotidienne)
    - [1. Configuration des variables d'environnement](#1-configuration-des-variables-denvironnement)
    - [2. Installation d'Ollama et du modèle gemma3:latest](#2-installation-dollama-et-du-modèle-gemma3latest)
- [Installer Ollama (Linux/macOS/Windows)](#installer-ollama-linuxmacoswindows)
- [Lancer Ollama (si ce n'est pas déjà fait)](#lancer-ollama-si-ce-nest-pas-déjà-fait)
- [Télécharger le modèle gemma3:latest](#télécharger-le-modèle-gemma3latest)
    - [3. Lancement du programme](#3-lancement-du-programme)

## Récupérer l'env

Pour récupérer et configurer l'environnement Python du projet, suivez ces étapes :

1. **Cloner le dépôt**  

  ```bash
  git clone https://github.com/Murcielago08/Projet_python_B3
  cd Projet_python_B3
  ```

2.**Créer un environnement virtuel**  

  ```bash
  python -m venv <env>
  ```

3.**Activer l'environnement virtuel**  

- Sur Windows :

    ```bash
    .\<env>\Scripts\activate
    ```

- Sur macOS/Linux :

    ```bash
    source <env>/bin/activate
    ```

4.**Installer les dépendances**  

  ```bash
  pip install -r requirements.txt
  ```

Votre environnement Python est maintenant prêt à l'emploi.

## Automatisation du support client e-commerce

## Cas pratique - Automatisation d'une veille quotidienne

Pour utiliser ce projet dans le cadre de l'automatisation d'une veille quotidienne, vous devez configurer les accès à Notion et à Ollama via des variables d'environnement.

### 1. Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet (dans le dossier veille_quoti_auto) ou configurer les variables suivantes :

- **Pour Notion :**
  - `NOTION_TOKEN` : votre token d'intégration Notion à créer ici [lien notion token](https://www.notion.so/profile/integrations) (ex : `secret_xxxxx...`)
  - `NOTION_DATABASE_ID` : copier le lien de votre page Notion cible 
    - exemple sur ce lien : https://www.notion.so/21e62387b3248010ae86c4b3dc86b5fc?v=21e62387b32480e7a32a000c7bfe55b8&source=copy_link on récupère ceci 21e62387b3248010ae86c4b3dc86b5fc

Exemple de fichier `.env` :
```env
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. Installation d'Ollama et du modèle gemma3:latest

Pour utiliser l'IA localement, vous devez installer Ollama et télécharger le modèle `gemma3:latest` :


# Installer Ollama (Linux/macOS/Windows)
[install ollama](https://ollama.com/download)

# Lancer Ollama (si ce n'est pas déjà fait)
```bash
ollama serve
```

# Télécharger le modèle gemma3:latest
```bash
ollama pull gemma3:latest
```

### 3. Lancement du programme

Activez votre environnement virtuel puis lancez le script principal :

```bash
python main.py
```

Lors de l'exécution, le programme vous demandera :
- **de choisir un thème** parmi la liste proposée (webdev, infosec, product, devops, founders, design, marketing, crypto, fintech, data) ou de saisir `all` pour récupérer tous les thèmes,
- **et d'entrer une date** au format AAAA-MM-JJ (ou appuyez sur Entrée pour utiliser la date du jour).

**Et voilà** 🎉

Tout est sur votre notion sauf les audios qui sont dans un dossier nommé *audios_acticles_xxxx_xx-xx-xx* 
