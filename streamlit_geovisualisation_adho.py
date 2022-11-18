#IMPORT LIBRARIES
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, Draw
from streamlit_folium import folium_static
import random

#IMPORT FICHIER CONTACTS AVEC DE VRAIES ADRESSES GEOCODEES (EN ATTENDANT DE POUVOIR REQUETER DES CONTACTS REELS)
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

#BARRE DE MENU LATERALE
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

carte_personnes = folium.Map(location=[47,2],zoom_start=6)

dico_nb_tags = {} #dictionnaire qui permet de comptabiliser les contacts dans chaque catégorie

def couleur_tag():
    """genere une couleur aleatoire"""
    r = lambda: random.randint(0,255)
    couleur_aleatoire ='#%02X%02X%02X' % (r(),r(),r())
    return couleur_aleatoire

def points_tag(tag):
    """ajoute sur la carte l'ensemble des contacts correspondant au tag"""
    couleur_du_tag = couleur_tag()
    df_points = df[df[tag]=='Oui']
    dico_nb_tags[tag] = df_points.shape[0]
    groupes = MarkerCluster()      #on clusterise les points
    for i in range(df_points.shape[0]):
        message = "<strong>" + df_points['first_name'].iloc[i] + ' ' + df_points['last_name'].iloc[i] + "</strong>"
        for j in range(df_points.shape[1]):
            if df_points.iloc[i,j]=='Oui':
                message += "<br>" + df_points.columns[j]
        latitude = df_points['Latitude'].iloc[i]
        longitude = df_points['Longitude'].iloc[i]
        mk = folium.CircleMarker([latitude, longitude], 
                                 radius = 5, 
                                 tooltip = message, 
                                 fill_color = couleur_du_tag, 
                                 fill_opacity=1,
                                 color=None)
        groupes.add_child(mk)
        groupes.add_to(carte_personnes)

#CUMULE LES POINTS DES TAGS SELECTIONNES
for tag in liste_tags:
    points_tag(tag)

contour = Draw(export=True, filename='mon_polygone.geojson')
contour.add_to(carte_personnes)
    
folium_static(carte_personnes) 

#AFFICHE LE NOMBRE DE CONTACTS DE CHAQUE TAG CHOISI ET LE TOTAL
for tag in liste_tags:
    st.write(tag, ':', dico_nb_tags[tag])
st.write('TOTAL', ':', sum(list(dico_nb_tags.values())))
