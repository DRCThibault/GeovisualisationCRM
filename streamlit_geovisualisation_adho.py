#IMPORT LIBRARIES
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import random

#IMPORT FICHIER CONTACTS
df = pd.read_csv("Fichier_contacts_geocode.csv", sep=';')

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

choix_menu = st.sidebar.radio('', options=parties_menu)

if choix_menu==parties_menu[0]:
    liste_categorie = liste_interet
if choix_menu==parties_menu[1]:
    liste_categorie = liste_donateur
if choix_menu==parties_menu[2]:
    liste_categorie = liste_petition
if choix_menu==parties_menu[3]:
    liste_categorie = liste_meeting


#CARTE DES PERSONNES INDIVIDUELLES
st.title(choix_menu)

liste_tags = st.multiselect("Indiquez les tags à visualiser :", liste_categorie)

carte_personnes = folium.Map(location=[47,2],zoom_start=6, tiles=None)

base_map = folium.FeatureGroup(name='Basemap', overlay=True, control=False)
folium.TileLayer().add_to(base_map)
base_map.add_to(carte_personnes)

def points_tag(tag):
    r = lambda: random.randint(0,255)
    couleur_choisie ='#%02X%02X%02X' % (r(),r(),r())
    df_points = df[df[tag]=='Oui'] 
    groupes = MarkerCluster()
    for i in range(df_points.shape[0]):
        message = "<strong>" + df_points['first_name'].iloc[i] + ' ' + df_points['last_name'].iloc[i] + "</strong>"
        for j in range(df_points.shape[1]):
            if df_points.iloc[i,j]=='Oui':
                message += "<br>" + df_points.columns[j]
        
        latitude = df_points['Latitude'].iloc[i]
        longitude = df_points['Longitude'].iloc[i]

        mk = folium.CircleMarker([latitude, longitude], radius = 5, tooltip = message, 
                        color=None, fill_color =couleur_choisie, fill_opacity=1)
        groupes.add_child(mk)
        groupes.add_to(carte_personnes)

for tag in liste_tags:
    points_tag(tag)

folium_static(carte_personnes) 

st.write('You selected:', liste_tags)
