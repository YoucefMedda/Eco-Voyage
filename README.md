# Eco-Voyage
Cette plateforme promeut le voyage éco-responsable en encourageant les pratiques touristiques respectueuses de la nature. Développée avec Django (frontend), HTML, CSS et JavaScript, elle vise à sensibiliser les voyageurs.

## 🚀 Lancer le projet en local

Ouvrez un terminal dans le dossier du projet et exécutez les commandes suivantes :

```bash
# 1. Créer un environnement virtuel
py -m venv venv

# 2. Activer l’environnement (sous Windows)
.\venv\Scripts\activate

# 3. Installer les dépendances
pip install django
pip install Pillow

# 4. Lancer le serveur de développement
py manage.py runserver
```



👉 Ouvrez ensuite votre navigateur et accédez à l'adresse suivante :
```bash
http://127.0.0.1:8000/
```

⚠️ Résolution des problèmes avec PowerShell
Si vous rencontrez des problèmes lors de l’exécution (ex : scripts bloqués), ouvrez PowerShell en tant qu’administrateur et exécutez :

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Pour revenir aux paramètres par défaut :

```bash
Set-ExecutionPolicy -ExecutionPolicy Default -Scope CurrentUser
```
