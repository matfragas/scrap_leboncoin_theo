# 🏡 Scraper Leboncoin - Détection automatique d'annonces

Ce projet est un projet à utitlisation **PERSONNELLE** il à pour but d'aider un ami dans sa recherche immobilière. C'est un **scraper automatique** pour **Leboncoin**, qui surveille les nouvelles annonces immobilières et envoie une **alerte par email** dès qu'une nouvelle annonce correspondant à tes critères apparaît.

## 🚀 Fonctionnalités
- ✅ **Scraping automatique** des annonces sur Leboncoin avec **Selenium**.
- ✅ **Stockage des annonces** dans un fichier `annonces.json` pour éviter les doublons.
- ✅ **Envoi d'un seul email** regroupant **toutes les nouvelles annonces**.
- ✅ **Exécution en continu** sur un Raspberry Pi.

---

## 📦 Installation

### 1️⃣ **Cloner le projet**
```bash
git clone https://github.com/Theo-lbd/Scrap_leboncoin
cd ton-repository
```

### 2️⃣ **Créer un environnement virtuel **
```bash
python3 -m venv venv
source venv/bin/activate  # Pour Linux/macOS
venv\Scripts\activate  # Pour Windows
```

### 3️⃣ **Installer les dépendances**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Configurer les variables d'environnement**
Crée un fichier `.env` et ajoute tes identifiants SMTP pour l'envoi d'email :
```plaintext
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
EMAIL_SENDER=ton-email@gmail.com
EMAIL_PASSWORD=ton-mot-de-passe
EMAIL_RECIPIENT=destinataire@gmail.com
```
**⚠️ Utilise un mot de passe d'application Gmail si nécessaire !** ([Créer un mot de passe d'application](https://myaccount.google.com/apppasswords))

---

## ▶️ **Utilisation**

### **1️⃣ Exécuter le script une seule fois**
```bash
python scraper.py
```
🔹 **Lors de la première exécution, toutes les annonces existantes sont enregistrées mais aucun email n'est envoyé.**  
🔹 **À chaque nouvelle exécution, seules les nouvelles annonces sont envoyées par email.**

---

## 🔄 **Exécution en continu sur un Raspberry Pi**

### **1️⃣ Lancer le script en arrière-plan avec `nohup`**
```bash
nohup python3 scraper.py &
```
- **Le script tourne en arrière-plan**, même si tu fermes le terminal.
- Les logs seront stockés dans `nohup.out`.

### **2️⃣ Automatiser l'exécution avec `cron` (au démarrage du Raspberry Pi)**
```bash
crontab -e
```
Ajoute cette ligne pour **exécuter le script au démarrage** :
```plaintext
@reboot /usr/bin/python3 /home/pi/ton-repository/scraper.py &
```

---

## 📜 **Fichiers et Structure du Projet**
```
📁 ton-repository/
│── scraper.py          # Script principal
│── config.py           # Configuration des paramètres
│── requirements.txt    # Dépendances Python
│── annonces.json       # Historique des annonces (créé automatiquement)
│── .gitignore          # Ignore les fichiers sensibles
│── .env                # Variables d'environnement (à créer)
│── README.md           # Documentation du projet
│── venv/               # (Optionnel) Environnement virtuel
```

---


## 👨‍💻 **Contribuer**
Si tu veux proposer une amélioration, n'hésite pas à ouvrir une issue ou à faire une pull request ! 🚀

---

