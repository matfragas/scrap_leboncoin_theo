from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import json
import time
from config import LEBONCOIN_URL, SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT


# Fichier pour stocker les annonces déjà vues
ANCIENNES_ANNONCES_FILE = "annonces.json"

# Charger les annonces déjà vues
try:
    with open(ANCIENNES_ANNONCES_FILE, "r") as f:
        anciennes_annonces = json.load(f)
except FileNotFoundError:
    anciennes_annonces = []

def setup_driver():
    """Configure Selenium WebDriver avec Chrome."""
    options = Options()
    options.add_argument("--headless")  # Mode sans interface graphique
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_annonces():
    """Scrape les annonces depuis Leboncoin."""
    driver = setup_driver()
    try:
        print("🔍 Chargement de la page...")
        driver.get(LEBONCOIN_URL)
        time.sleep(5)  # Laisser la page se charger complètement

        # Vérifie si la page contient des éléments attendus
        if "Aucune annonce" in driver.page_source:
            print("✅ Connexion réussie, mais aucune annonce trouvée.")
        else:
            print("✅ Connexion réussie, des annonces sont disponibles.")
        
        # Récupérer le HTML rendu par Selenium
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Extraire les annonces
        annonces = []
        for annonce in soup.find_all("li", class_="styles_adCard__klAb3"):
            try:
                titre = annonce.find("h2", class_="text-body-2").text.strip()
                prix = annonce.find("p", class_="text-callout").text.strip()
                lien = "https://www.leboncoin.fr" + annonce.find("a")["href"]
                annonces.append({"titre": titre, "lien": lien, "prix": prix})
            except AttributeError:
                # Ignore les annonces mal formatées
                continue

        print(f"🔍 {len(annonces)} annonces récupérées.")
        for annonce in annonces[:5]:  # Affiche les 5 premières annonces
            print(f"🏠 {annonce['titre']} - {annonce['prix']} - {annonce['lien']}")

        return annonces

    except Exception as e:
        print(f"❌ Erreur lors du scraping : {e}")
    finally:
        driver.quit()

def sauvegarder_annonces(annonces):
    try:
        with open(ANCIENNES_ANNONCES_FILE, "r") as f:
            anciennes_annonces = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        anciennes_annonces = []

    nouvelles_annonces = [a for a in annonces if a["lien"] not in [x["lien"] for x in anciennes_annonces]]
    
    if nouvelles_annonces:
        anciennes_annonces.extend(nouvelles_annonces)
        with open(ANCIENNES_ANNONCES_FILE, "w") as f:
            json.dump(anciennes_annonces, f, indent=4)

        print(f"✅ {len(nouvelles_annonces)} nouvelles annonces enregistrées.")


def envoyer_notification(annonce):
    """Affiche une notification dans la console (remplace par l'email si nécessaire)."""
    print(f"🆕 Nouvelle annonce détectée : {annonce['titre']} - {annonce['prix']}")
    print(f"🔗 {annonce['lien']}")

def verifier_nouvelles_annonces():
    """Vérifie les nouvelles annonces et envoie une seule notification regroupée."""
    print("🔍 Vérification des nouvelles annonces...")
    nouvelles_annonces = get_annonces()

    # Charger les annonces déjà vues depuis le fichier
    try:
        with open(ANCIENNES_ANNONCES_FILE, "r") as f:
            anciennes_annonces = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        anciennes_annonces = []

    # Filtrer uniquement les nouvelles annonces
    nouvelles_annonces_a_envoyer = [a for a in nouvelles_annonces if a["lien"] not in [x["lien"] for x in anciennes_annonces]]

    if nouvelles_annonces_a_envoyer:
        # Envoyer un seul email avec toutes les nouvelles annonces
        envoyer_email(nouvelles_annonces_a_envoyer)

        # Sauvegarde des nouvelles annonces dans le fichier JSON
        anciennes_annonces.extend(nouvelles_annonces_a_envoyer)
        with open(ANCIENNES_ANNONCES_FILE, "w") as f:
            json.dump(anciennes_annonces, f, indent=4)

        print(f"✅ {len(nouvelles_annonces_a_envoyer)} nouvelles annonces enregistrées et envoyées par email.")
    else:
        print("📭 Aucune nouvelle annonce détectée.")

    print("✅ Vérification terminée.")




def envoyer_email(annonces):
    """Envoie un email regroupant toutes les nouvelles annonces."""
    if not annonces:
        print("📭 Aucune nouvelle annonce à envoyer.")
        return

    sujet = f"🏡 {len(annonces)} nouvelles annonces sur Leboncoin"
    
    message = "🔍 Voici la liste des nouvelles annonces :\n\n"
    for annonce in annonces:
        message += f"🏠 {annonce['titre']} - {annonce['prix']}\n🔗 {annonce['lien']}\n\n"

    msg = MIMEText(message)
    msg["Subject"] = sujet
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        print(f"✅ Email envoyé avec {len(annonces)} nouvelles annonces.")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email : {e}")

while True:
    verifier_nouvelles_annonces()
    print("⏳ Attente de 5 minutes avant la prochaine vérification...")
    time.sleep(300)  # 5 minutes
