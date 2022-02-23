#%% Imports
import folium
from folium import plugins
from folium.plugins.marker_cluster import MarkerCluster
import json
import requests
import numpy as np
import pandas as pd
import math



#%% Lecture des données 
df_villes = pd.read_csv('codesinseecommunesgeolocalisees.csv', encoding='utf-8', sep=",")
df_villes["longitude"] = df_villes["longitude_radian"] * 180 / math.pi
df_villes["latitude"] = df_villes["latitude_radian"] * 180 / math.pi
#['Insee', 'Nom', 'Altitude', 'code_postal', 'longitude_radian',
# 'latitude_radian', 'pop99', 'surface', 'longitude', 'latitude']

# df_villes = pd.read_csv('ville.csv', encoding='utf-8', sep=";")

url_json = requests.get("https://presidentielle2022.conseil-constitutionnel.fr/telechargement/parrainagestotal.json")
url_json.encoding = 'utf-8-sig'
parains = json.loads(url_json.text)

# Conversion en Dataframe
df_parains = pd.DataFrame(parains)
# ['Civilite', 'Nom', 'Prenom', 'Mandat', 'Circonscription', 'Departement',
#  'Candidat', 'DatePublication']

# Couleurs des candidats
l_couleurs = {"PÉCRESSE Valérie" : "darkblue",
"MACRON Emmanuel" : "blue",
"HIDALGO Anne" : "pink",
"ROUSSEL Fabien" : "red",
"JADOT Yannick" : "green",
"LASSALLE Jean" : "lightblue",
"ARTHAUD Nathalie" : "lightred",
"MÉLENCHON Jean-Luc" : "darkred",
"DUPONT-AIGNAN Nicolas" : "cadetblue",
"LE PEN Marine" : "beige",
"ZEMMOUR Éric" : "white",
"ASSELINEAU François" : "purple",
"POUTOU Philippe" : "orange",
"KAZIB Anasse" : "gray",
"TAUBIRA Christiane" : "darkpurple",
"THOUY Hélène" : "gray",
"KUZMANOVIC Georges" : "lightgray",
"KOENIG Gaspard" : "lightgray",
"EGGER Clara" : "lightgray",
"MIGUET Nicolas" : "lightgray",
"MARTINEZ Antoine" : "lightgray",
"CHICHE Arnaud" : "lightgray",
"SMATI  Rafik" : "lightgray",
"FORTANÉ Jean-Marc" : "lightgray",
"ROCCA Martin" : "lightgray",
"WAECHTER Antoine" : "lightgray",
"CAU Marie" : "lightgray",
"BÉKAERT Corinne" : "lightgray",
"RIVOAL Stéphanie" : "lightgray",
"MAZUEL Philippe" : "lightgray",
"MÉNARD Emmanuelle" : "lightgray",
"ROCQUEMONT Antoine" : "lightgray",
"CAHEZ Thierry" : "lightgray",
"FIORILE Eric Régis" : "lightgray",
"DELGA Carole" : "lightgray",
"WENDLINGER Stéphane" : "lightgray",
"BARNIER Michel" : "lightgray",
"MEURICE Guillaume" : "lightgray",
"LAM Yaya" : "lightgray",
"SCHOVANEC Josef" : "lightgray",
"HOLLANDE François" : "lightgray",
"COJAN Patrick" : "lightgray",
"VIEIRA Gildas" : "lightgray",
"PHILIPPOT Florian" : "lightgray",
"FESSARD DE FOUCAULT Bertrand" : "lightgray",
"MARECHAL Philippe Célestin" : "lightgray",
"SAINT-PAUL Laetitia" : "lightgray"}

#%% Appariemment des données
is_maire = df_parains.Mandat.str.contains('Maire')
df_maires = pd.merge(df_villes, df_parains[is_maire], 
                     left_on='Nom', right_on='Circonscription', 
                     how="left")

#%% Préparation des données 
data_sites = []
has_parain = [isinstance(value, str) for value in df_maires['Civilite']]

for idx, row in df_maires.iterrows():
    item = {"status": "Parrains" if has_parain[idx] else "*",
    "candidat": row['Candidat'] if has_parain[idx] else "Autre",
    "coordinates" : [row['latitude'], row['longitude']], 
    "commune":row['Nom_x'], 
    "couleur": l_couleurs[row['Candidat']] if has_parain[idx] else "gray",
    "infos":(f"Ville : {row['Nom_x']}<br/>Maire:{row['Nom_y']}<br/> → {row['Candidat']} " if  has_parain[idx] else f"Ville : {row['Nom_x']}<br/>Pas de parrainage")
    }
    data_sites.append(item)


#%% Création de la carte
m = folium.Map(location=[46.7687714,4.5660859], 
    zoom_start=6.21, 
    max_zoom=18, min_zoom=1,
    tiles='OpenStreetMap')

#%% Constitution des groupes
mcg = folium.plugins.MarkerCluster(control=False)   # Marker Cluster, hidden in controls
m.add_child(mcg)


# Ajout des groupes
bSansParrain = False
groups = {"PÉCRESSE": None,"MACRON":None,"HIDALGO":None,"ROUSSEL":None,"JADOT":None,
"LASSALLE":None,"ARTHAUD":None,"MÉLENCHON":None, "DUPONT-AIGNAN":None, "LE PEN":None,
"ZEMMOUR":None, "ASSELINEAU":None,"POUTOU":None,"KAZIB":None,"TAUBIRA":None, 'Autre':None}

if bSansParrain:
    groups['Pas de parrainage'] = None

g_keys = groups.keys()

for k in g_keys:
    groups[k] = folium.plugins.FeatureGroupSubGroup(mcg, k)
    m.add_child(groups[k])

for site in data_sites:
    if site["status"]=="Parrains":
        mark = folium.Marker(site["coordinates"],popup=site["infos"], tooltip=site["infos"], icon=folium.Icon(color=site["couleur"], icon='ok-sign'))
        l_k = [k for k in g_keys if k in site["candidat"]]
        k = l_k[0] if len(l_k) else 'Autre'
        groups[k].add_child(mark)
    elif bSansParrain:
        mark = folium.Marker(site["coordinates"],popup=site["infos"], tooltip=site["infos"],icon = folium.Icon(color=site["couleur"], icon='exclamation-sign'))
        groups['Pas de parrainage'].add_child(mark)

folium.LayerControl().add_to(m)


#%% Sauvegarde de la carte
m.save("index.html")

# %%
