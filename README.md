# Évaluation Python B2

API REST de gestion de stations réalisée avec FastAPI, SQLAlchemy et SQLite.

## Structure du projet


eval-othmane-laguelil-b2/
├── app/
│   └── main.py
├── tests/
│   └── test_stations.py
├── requirements.txt
├── README.md
├── reponses.md
└── .gitignore


## Installation

### 1. Créer l'environnement virtuel


python -m venv .venv


### 2. Activer l'environnement virtuel

Sous Git Bash :

```bash
source .venv/Scripts/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancer l'API

Depuis la racine du projet :

```bash
uvicorn app.main:app --reload
```

L'API est disponible à l'adresse :


http://127.0.0.1:8000


## Documentation Swagger

La documentation interactive de l'API est disponible ici :


http://127.0.0.1:8000/docs


## Routes principales

### Vérification de l'API


GET /health


### Créer une station


POST /stations


Exemple :


{
  "code": "ST001",
  "name": "Gare",
  "capacity": 20,
  "status": "open"
}


### Récupérer les stations


GET /stations


### Filtrer les stations par statut


GET /stations?status=open


Les statuts possibles sont :


open
closed
maintenance


### Récupérer une station


GET /stations/{station_id}


### Modifier une station


PATCH /stations/{station_id}


Exemple :


{
  "name": "Nouvelle Gare",
  "status": "closed"
}


## Base de données

L'application utilise une base de données SQLite :


stations.db


La base est créée automatiquement au lancement de l'application grâce à SQLAlchemy.

Les bases de données sont exclues du dépôt Git grâce au fichier `.gitignore`.

## Tests

Les tests utilisent `pytest` et `TestClient`.

Pour lancer tous les tests :


python -m pytest -q


Les tests vérifient notamment :

la création d'une station ; le refus d'un code déjà existant ;la gestion d'une station inexistante ; la validation des données ; la modification d'une station ; le filtrage des stations par statut.

## GitHub

Le projet doit être enregistré dans un dépôt nommé :


eval-nom-prenom-python-b2


Les éléments suivants ne doivent pas être envoyés sur GitHub :


.venv/
__pycache__/
*.pyc
.pytest_cache/
*.db

l exo 4 fais avec de l ia 
