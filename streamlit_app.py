import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Titre de l'application
st.title("Génération de Google Sheets")

# Renseignez ici les informations de votre fichier de service Google Sheets
credentials = ServiceAccountCredentials.from_json_keyfile_name("streamlit-386323-ba71a712bde5.json", ['https://www.googleapis.com/auth/drive'])
client = gspread.authorize(credentials)

# Sélection du répertoire contenant les fichiers Excel
folder_path = "Streamlit/exemple-Export-Semrush/uplix-2023-audit/Current"

# Bouton pour générer le Google Sheet
if st.button("Générer le Google Sheet"):
    # Vérifier si le chemin du dossier est valide
    if not os.path.isdir(folder_path):
        st.error("Chemin de dossier invalide.")
        st.stop()
    
    # Fonction de génération du tableau de mots-clés
    def generate_keywords_table(folder_path):
        dfs = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".xlsx"):
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_excel(file_path)
                dfs.append(df)
        
        if not dfs:
            st.error("Aucun fichier Excel trouvé dans le dossier.")
            return None
        
        combined_df = pd.concat(dfs)
        selected_columns = ['Keyword', 'Position', 'URL']
        keywords_table = combined_df[selected_columns]

        return keywords_table
    
    keywords_table = generate_keywords_table(folder_path)
    
    if keywords_table is not None:
        # Création du nouveau fichier Google Sheets
        new_sheet = client.create("Tableau de mots-clés")
        worksheet = new_sheet.get_worksheet(0)

        # Enregistrement des données dans le Google Sheets
        data = [keywords_table.columns.tolist()] + keywords_table.values.tolist()
        worksheet.update(data)

        st.success("Le Google Sheet a été généré avec succès.")

        # Affichage du lien vers le Google Sheet généré
        st.write("Lien vers le Google Sheet généré :")
        st.write(new_sheet.url)
