

# Jeu du Pendu avec Python, Flask et MySQL

## Vue d'ensemble
Ce projet est un jeu du Pendu développé en utilisant Python pour la logique du jeu, Flask pour l'API, et MySQL pour le stockage des données. Le jeu permet aux utilisateurs de deviner les lettres d'un mot, et leurs données de jeu sont stockées dans une base de données. Le projet est structuré de manière à permettre des extensions futures, telles que des points de terminaison API supplémentaires ou des fonctionnalités de jeu plus complexes.

## Fonctionnalités
- Logique centrale du jeu du Pendu implémentée en Python.
- Serveur API basé sur Flask.
- Intégration d'une base de données MySQL pour un stockage persistant des données.
- Structure modulaire du projet pour une maintenance et une évolutivité aisées.

## Structure du projet
```
hangman_game/
├── database/
│   ├── __pycache__/           
│   ├── backup/                
│   ├── api_server.py          
│   └── db_connection.py       
├── game/
│   └── Hangman.py
│      └── README.md
         

## Installation

### Prérequis
- Python 3.x
- Base de données MySQL

### Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/yourusername/hangman_game.git
   cd hangman_game
   ```

2. Configurer MySQL :
   - Créez une base de données MySQL pour le jeu.
   - Mettez à jour `db_connection.py` avec vos identifiants de base de données.

3. Lancer l'API Flask :
   Pour démarrer le serveur Flask, exécutez :
   ```bash
   python database/api_server.py
   ```

4. Exécuter le jeu du Pendu :
   Pour exécuter directement la logique du jeu (version CLI) :
   ```bash
   python game/Hangman.py
   ```



