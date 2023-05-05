import semrush
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurer les identifiants d'authentification pour l'API Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Ouvrir la feuille de calcul Google Sheets
sheet = client.open('Ma feuille de calcul').sheet1

# Récupérer les informations sur le mot clé à partir de l'API SEMrush
api_key = 'ma_clé_api_semush'
domain = 'mon_domaine.com'
keyword = 'mon_mot_clé'
result = semrush.DomainOverview(domain, api_key=api_key, display_limit=10)
data = result['Rankings']['Organic']

# Créer un DataFrame Pandas à partir des données récupérées
df = pd.DataFrame(data)

# Écrire les données sur la feuille de calcul Google Sheets
sheet.clear()
sheet.update([df.columns.values.tolist()] + df.values.tolist())
