import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Titre de l'application
st.title("Génération de Google Sheets")

# Renseignez ici les informations de votre fichier de service Google Sheets
credentials = ServiceAccountCredentials.from_json_keyfile_name("streamlit-386418-0f7348939df2.json", ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(credentials)

# Champ de saisie pour le nom du fichier Google Sheets
sheet_name = st.text_input("Nom du fichier Google Sheets :")

# Champ de saisie pour les données à enregistrer
data_input = st.text_area("Données à enregistrer (une ligne par donnée) :")

# Bouton pour générer le Google Sheets
if st.button("Générer le Google Sheets"):
    # Création du nouveau fichier Google Sheets
    new_sheet = client.create(sheet_name)
    worksheet = new_sheet.get_worksheet(0)
    
    # Enregistrement des données dans le Google Sheets
    data = data_input.split('\n')
    for i, item in enumerate(data):
        worksheet.update_cell(i+1, 1, item)
    
    st.success("Le Google Sheets a été généré avec succès.")

# Affichage du lien vers le Google Sheets généré
if 'new_sheet' in locals():
    st.write("Lien vers le Google Sheets généré :")
    st.write(new_sheet.url)
