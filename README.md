# Test à réaliser

### Setup

git clone
python -m venv env ==> dans le dossier cloné pour créer un environnement virtuel pour le projet
source env/bin/activate ==> pour activer l'environnement depuis la racine du projet.
pip install -r requirements.txt ==> pour installer les dépendances nécessaires.
python manage.py migrate ==> pour initialiser la base de données
renseigner le superUser de la BDD dans api/management/commands/init_db.py
python manage.py init_db ==> pour peupler la base de données
