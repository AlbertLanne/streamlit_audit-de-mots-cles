import streamlit as st
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Titre de l'application
st.title("Audit de mots clés")

# Renseignez ici les informations de votre fichier de service Google Sheets
credentials = ServiceAccountCredentials.from_json_keyfile_name("streamlit-386323-6eccb7ac6d66.json", ["https://spreadsheets.google.com/feeds"])
client = gspread.authorize(credentials)
sheet = client.open("Sumrush Sheet").sheet1

# Champ de saisie pour le mot clé
keyword = st.text_input("Renseignez le mot clé :")

# Bouton pour lancer l'audit
if st.button("Lancer l'audit"):
    # URL du site SEMrush pour effectuer la recherche du mot clé
    url = f"https://www.semrush.com/fr/info/{keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Récupération des informations souhaitées depuis le site SEMrush
    volume_global = soup.find("div", class_="seo-parameters__value js-seo-volume-global")
    cpc = soup.find("div", class_="seo-parameters__value js-seo-cpc")
    concurrence = soup.find("div", class_="seo-parameters__value js-seo-competition")

    # Affichage des informations
    if volume_global and cpc and concurrence:
        st.write("Résultats de l'audit :")
        st.write(f"Volume de recherche global : {volume_global.text.strip()}")
        st.write(f"CPC (Coût Par Clic) : {cpc.text.strip()}")
        st.write(f"Concurrence : {concurrence.text.strip()}")

        # Écriture des informations dans la feuille de calcul Google Sheets
        sheet.append_row([keyword, volume_global.text.strip(), cpc.text.strip(), concurrence.text.strip()])
        st.write("Les informations ont été enregistrées dans la feuille de calcul Google Sheets.")
    else:
        st.write("Aucun résultat trouvé pour ce mot clé.")






