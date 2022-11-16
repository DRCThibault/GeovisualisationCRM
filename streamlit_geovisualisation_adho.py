#IMPORT LIBRARIES
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

#IMPORT FICHIER CONTACTS
df = pd.read_excel("Fichier_contacts_geocode.xlsx")

#LISTES DES CATEGORIES
liste_interet = ['IntérêtDéfense',
                 'IntérêtÉconomie',
                 'IntérêtÉducation',
                 'IntérêtGéopolitique',
                 'CentreIntérêtLaCouture',
                 'CentreIntérêtLeVélo',
                 'CentreIntérêtLaCuisine',
                 'CentreIntérêtLesVoyages',
                 'CentreIntérêtRien']
liste_donateur = ['donateur10', 
                  'donateur20', 
                  'donateur50', 
                  'donateur100']
liste_petition = ['PetitionSauvezWilly',
                 'PetitionSouleverDesMontagne',
                 'PetitionVieDureSansConfiture']
liste_meeting = ['MeetingGrandMeetingDeLaRentree2022',
                 'MeetingLesRencontresMensuelles',
                 'MeetingManifestationContreLeauFroide',
                 'MeetingManifestationContreLeFeu']

st.sidebar.title("Catégories")
st.sidebar.subheader("Menu")

parties_menu = ["Centres d'intérêt",
                "Donateurs",
                "Pétitions",
                "Meetings"]


liste_categorie = st.sidebar.radio('', options=parties_menu)