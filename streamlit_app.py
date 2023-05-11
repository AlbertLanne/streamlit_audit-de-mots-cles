import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Renseignez ici les informations de votre fichier Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('streamlit-386323-6eccb7ac6d66.json', scope)
client = gspread.authorize(credentials)
sheet = client.open('Sheet Sumrush').sheet1

# Renseignez ici votre mot-clé
mot_cle = "votre_mot_cle"

# URL de recherche SEMrush pour le mot-clé spécifié
url = f"https://www.semrush.com/analytics/seo/overview/?q={mot_cle}"

# Effectuer une requête GET pour obtenir la page de résultats SEMrush
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extraire les informations souhaitées de la page
infos = []
elements = soup.find_all('div', class_='key-value-Block__value')

for element in elements:
    infos.append(element.get_text().strip())

# Écrire les informations dans le fichier Google Sheets
row = [mot_cle] + infos
sheet.append_row(row)

print("Données enregistrées avec succès dans Google Sheets.")
