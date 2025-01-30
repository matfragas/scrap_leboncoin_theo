import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# URL de recherche Leboncoin
LEBONCOIN_URL = "https://www.leboncoin.fr/recherche?category=9&text=maison&locations=Nantes_44000"

# Email de notification (si utilisé)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
