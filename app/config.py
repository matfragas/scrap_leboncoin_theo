import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# URL de recherche Leboncoin
#LEBONCOIN_URL = "https://www.leboncoin.fr/recherche?category=9&text=maison&locations=Moissac_82200,Castelsarrasin_82100&price=min-150000&real_estate_type=1,2,5&immo_sell_type=old"
LEBONCOIN_URL = "https://www.leboncoin.fr/recherche?category=9&text=maison&locations=L%27Huisserie_53970__48.02281_-0.77001_5000,Louvern%C3%A9_53950__48.12273_-0.72003_5000,Saint-Berthevin_53940__48.06967_-0.83152_5000,Chang%C3%A9_53810__48.09901_-0.78975_5000,Laval_53000__48.07268_-0.77307_5000&price=min-340000&land_plot_surface=85-max&real_estate_type=1&immo_sell_type=old,new"

# Email de notification (si utilisé)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
