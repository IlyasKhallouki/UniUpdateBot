# UniUpdateBot README pour le Personnel Scolaire

## Introduction
UniUpdateBot est un scraper web automatisé convivial conçu pour le personnel scolaire afin de surveiller le site web de l'université en temps réel. Il simplifie le processus de diffusion d'informations opportunes en extrayant les mises à jour et en envoyant des notifications structurées par e-mail aux étudiants et aux professeurs. Aucune connaissance technique avancée n'est requise; il suffit de configurer les fichiers `emails.xlsx` et `Date Tracker.csv`, de configurer le fichier `.env` et le dossier `Attachments` pour commencer.

## Configuration et Installation

### 1. `emails.xlsx`
Ce fichier Excel doit contenir la liste des destinataires des e-mails. Assurez-vous de structurer le fichier Excel avec des en-têtes de colonnes appropriés pour les noms et les adresses e-mail, et modifiez `sender.py` en conséquence.

### 2. `Date Tracker.csv`
Le fichier `Date Tracker.csv` garde une trace des derniers moments de mise à jour pour éviter les notifications en double. Mettez à jour le fichier avec les dates les plus récentes au besoin.

### 3. Configuration du fichier `.env`
Le fichier `.env` est l'endroit où des informations sensibles telles que les informations de connexion et les clés API sont stockées. Suivez le modèle fourni pour remplir les champs nécessaires :

```plaintext
OPENAI_API_KEY= Votre clé API OpenAI
EMAIL_ADDRESS= Votre adresse e-mail
EMAIL_PASSWORD= Le mot de passe à 2F de votre e-mail
```

### 4. Dossier des Pièces Jointes
Créez un dossier nommé `Attachments` où les pièces jointes seront stockées.

## Syntaxe des Balises
Chaque article destiné à être publié doit contenir des balises qui permettront au bot de le détecter et de l'envoyer.

- **Pour envoyer un article :** `#SEND#`
- **Pour spécifier à qui est destiné l'e-mail :** `#TO:CIBLE,SÉPARÉE,PAR,VIRGULE#S`
- **Cibles disponibles :** ALL, GC, GI, IATE, DWM, GIM, GTE, GE, CPA, TCC, GRH, FBA, LM, LP, PROF
- **Syntaxe HTML pour ajouter des balises :**
  ```html
  <p id="invisible-text" style="display: none;">#SEND# #TO:(Cibles)#</p>
  ```

## Utilisation et Maintenance
Pour lancer le bot, exécutez simplement `scraper.py`. Malheureusement, la fiabilité du modèle GPT d'OpenAI n'est pas suffisante pour fonctionner de manière autonome ; c'est pourquoi le bot a besoin d'une personne pour agir en tant que superviseur. À chaque rédaction d'un nouvel e-mail, une nouvelle fenêtre MSWord s'ouvre pour permettre au superviseur d'apporter des modifications si nécessaire.

---

*Remarque : Le README fournit des instructions détaillées pour la configuration de UniUpdateBot. Pour toute assistance supplémentaire ou questions, n'hésitez pas à me contacter*

