# V2 sur un fichier de villes/localisation d'une autre source
#%% Imports
import folium
from folium import plugins
from folium.plugins.marker_cluster import MarkerCluster
import json
import requests
import numpy as np
import pandas as pd
from random import random
import unicodedata
import math

# Fonctions utilitaires pour supprimer les accents
# Sur un dataframe
prep_string_df = lambda x: x.str.normalize('NFKD').str.replace("œ","oe").str.encode('ascii', errors='ignore').str.decode('utf-8').str.replace('-',' ').str.replace("'",' ').str.upper()
# Sur une chaine
prep_string = lambda x: unicodedata.normalize('NFKD',x).replace("œ","oe").encode('ascii', errors='ignore').decode('utf-8').replace('-',' ').replace("'",' ').upper()


#%% Lecture des données

#  Fichier eucircos
df_regions = pd.read_csv('eucircos_regions_departements_circonscriptions_communes_gps.csv', encoding='utf-8', sep=";", 
dtype={'nom_département': str, 'codes_postaux':str, 'latitude':float, 'longitude':float})
#['EU_circo', 'code_région', 'nom_région', 'chef-lieu_région','numéro_département', 'nom_département', 'préfecture', 
# 'numéro_circonscription', 'nom_commune', 'codes_postaux', 'code_insee', 'latitude', 'longitude', 'éloignement']
df_regions['COM'] = prep_string_df(df_regions['nom_commune'])
df_regions['DEP'] = prep_string_df(df_regions['nom_département'])
df_regions['REG'] = prep_string_df(df_regions['nom_région'])



#%% Fichier INSEE
df_insee = pd.read_csv('codesinseecommunesgeolocalisees.csv', encoding='utf-8', sep=",")
df_insee["longitude"] = df_insee["longitude_radian"] * 180 / math.pi
df_insee["latitude"] = df_insee["latitude_radian"] * 180 / math.pi
df_insee.drop(['latitude_radian', 'longitude_radian'], axis=1, inplace=True)
df_insee['COM'] = prep_string_df(df_insee['Nom'])
#['Insee', 'Nom', 'Altitude', 'code_postal', 'longitude_radian',
# 'latitude_radian', 'pop99', 'surface', 'longitude', 'latitude']

#%% Fichier la poste
df_poste = pd.read_csv('laposte_hexasmal.csv', encoding='utf-8', sep=";", 
dtype={'Code_postal':str, 'latitude':float, 'longitude':float})

df_poste['numéro_département'] = df_poste['Code_commune_INSEE'].apply(lambda x : x[0:3] if x.startswith('97') or x.startswith('98') else x[0:2])

# Code_commune_INSEE;Nom_commune;Code_postal;Ligne_5;Libellé_d_acheminement;latitude;longitude
df_poste.drop(['Ligne_5', 'Libellé_d_acheminement'], axis=1, inplace=True)
df_poste.drop_duplicates(inplace=True)

# On ajoute les départements dans df_poste
df_poste = pd.merge(df_poste,
             df_regions[['numéro_département','nom_département']].drop_duplicates(), 
             how='left', on='numéro_département')

# Colonne pour recherche
df_poste['COM'] = prep_string_df(df_poste['Nom_commune'])
df_poste['DEP'] = prep_string_df(df_poste['nom_département'])

#%% Chargement données conseil constitutionnel
url_json = requests.get("https://presidentielle2022.conseil-constitutionnel.fr/telechargement/parrainagestotal.json")
url_json.encoding = 'utf-8-sig'
parains = json.loads(url_json.text)

# Conversion en Dataframe
df_parains = pd.DataFrame(parains)
# ['Civilite', 'Nom', 'Prenom', 'Mandat', 'Circonscription', 'Departement', 'Candidat', 'DatePublication']
# Colonnes pour recherche
df_parains['COM'] = prep_string_df(df_parains['Circonscription'])
df_parains['DEP'] = prep_string_df(df_parains['Departement'])


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
"SAINT-PAUL Laetitia" : "lightgray",
"LAURUT Christian" : "lightgray",
"ROCQUEMONT Antoine" : "lightgray", 
"BORLOO Jean-Louis" : "lightgray",
"MONTEBOURG Arnaud" : "lightgray"}


#%% Appariemment des données bis
# Au cas par cas pour retrouver les lieux par type de Mandats, les principaux sont :
df_parains['Mandat'].value_counts()
# Maire                                                                                      6086
# Conseillère départementale                                                                  656
# Conseiller départemental                                                                    563
# Conseillère régionale                                                                       476
# Conseiller régional                                                                         424
# Député                                                                                      270
# Maire délégué d'une commune associée ou d'une commune déléguée                              209
# Députée                                                                                     201
# Sénateur                                                                                    155
# Sénatrice                                                                                    93
# Maire déléguée d'une commune associée ou d'une commune déléguée                              76

data_sites = []
n_com_ko = 0
n_reg_ko = 0
n_dep_ko = 0
n_deput_ko = 0
n_autre_ko = 0
n_arrond_ko = 0
cpt_fe = 0 # Français à l'étranger en grille ...
for idx, row in df_parains.iterrows():
    # Offset de position GPS pour éviter les points identiques
    offset = [(0.5-random())*0, (0.5-random())*0]

    # Test des différents cas
    if "FRANCAIS DE L ETRANGER" in row['DEP']:
        # Français de l'étranger : au milieu de l'atlantique
        coords = [31.623596, -43.779435]
        info = f"{row['Departement']}/{row['Circonscription']}<br/>{row['Mandat']} : {row['Civilite']} {row['Prenom']} {row['Nom']}"
        cpt_fe = cpt_fe + 1

    elif any(s in row['Mandat'] for s in ['arrondissement', 'de Paris']):
        # Recherche DEP & coordonnées du chef-lieu 'nom_région', 'chef-lieu_région'
        df_d = df_regions[df_regions['COM']==row['DEP']]
        if len(df_d):
            # Recherche de la préfecture
            df_v = df_d[prep_string_df(df_d['chef-lieu_région'])==df_d['COM']]
            coords = [df_v.iloc[0]['latitude']+offset[0], df_v.iloc[0]['longitude']+ offset[1]]
            info = f"{row['Circonscription']}/{row['Departement']}<br />{row['Mandat']}<br /> {row['Civilite']} {row['Prenom']} {row['Nom']}"
        else:
            df_d = df_regions[df_regions['DEP']==row['DEP']]
            if len(df_d):
                # Recherche de la préfecture
                df_v = df_d[prep_string_df(df_d['préfecture'])==df_d['COM']]
                coords = [df_v.iloc[0]['latitude']+offset[0], df_v.iloc[0]['longitude']+offset[1]]
                info = f"{row['Departement']}<br/>{row['Mandat']} : {row['Civilite']} {row['Prenom']} {row['Nom']}"
            else:
                print(f"!!! KO 'arrondissement'.... : {', '.join(row)}")
                n_arrond_ko = n_arrond_ko + 1
                continue

    elif 'Maire' in row['Mandat']:
        # Recherche de la ville dans le département (disambiguation)
        # 1:fichier la poste
        df_v = df_poste[np.logical_and(df_poste['COM']==row['COM'], df_poste['DEP']==row['DEP'])]
        if len(df_v):
            coords = [df_v.iloc[0]['latitude'], df_v.iloc[0]['longitude']]
            info = f"Ville : {row['Circonscription']}/{row['Departement']}<br/>{row['Mandat']} : {row['Civilite']} {row['Prenom']} {row['Nom']}"
        else:
            # 2: fichier insee
            df_v = df_insee[df_insee['COM']==row['COM']]
            if len(df_v):
                coords = [df_v.iloc[0]['latitude'], df_v.iloc[0]['longitude']]
                info = f"Ville : {row['Circonscription']}/{row['Departement']}<br/>{row['Mandat']} : {row['Civilite']} {row['Prenom']} {row['Nom']}"
            else:
                print(f"!!! KO 'Maire' : {', '.join(row)}")
                n_com_ko = n_com_ko + 1
                continue

    elif any(s in row['Mandat'] for s in ['métropolitain', 'départemental', 'Député', 'Sénateur', 'Sénatrice', 'EPCI' ]):
        # Recherche du département & coordonnées de la préfecture
        df_d = df_regions[df_regions['DEP']==row['DEP']]
        if len(df_d):
            # Recherche de la préfecture
            df_v = df_d[prep_string_df(df_d['préfecture'])==df_d['COM']]
            coords = [df_v.iloc[0]['latitude']+offset[0], df_v.iloc[0]['longitude']+offset[1]]
            info = f"{row['Departement']}<br/>{row['Mandat']} : {row['Civilite']} {row['Prenom']} {row['Nom']}"
        else:
            print(f"!!! KO 'métropolitain',... : {', '.join(row)}")
            n_deput_ko = n_deput_ko + 1
            continue

    elif 'régional' in row['Mandat']:
        # Recherche région & coordonnées du chef-lieu 'nom_région', 'chef-lieu_région'
        df_d = df_regions[df_regions['REG']==row['COM']]
        if len(df_d):
            # Recherche de la préfecture
            df_v = df_d[prep_string_df(df_d['chef-lieu_région'])==df_d['COM']]
            coords = [df_v.iloc[0]['latitude']+offset[0], df_v.iloc[0]['longitude']+offset[1]]
            info = f"{row['Circonscription']}/{row['Departement']}<br/>{row['Mandat']} : {row['Civilite']} {row['Prenom']} {row['Nom']}"
        else:
            print(f"!!! KO 'régional' : {', '.join(row)}")
            n_reg_ko = n_reg_ko + 1
            continue

    elif 'outre-mer' in row['Mandat']:
        # Recherche région & coordonnées du chef-lieu 'nom_région', 'chef-lieu_région'
        df_d = df_regions[np.logical_or(df_regions['REG']==row['COM'], df_regions['REG']==row['DEP'])]
        if len(df_d):
            # Recherche de la préfecture
            df_v = df_d[prep_string_df(df_d['chef-lieu_région'])==df_d['COM']]
            coords = [df_v.iloc[0]['latitude']+offset[0], df_v.iloc[0]['longitude']+offset[1]]
            info = f"{row['Circonscription']}/{row['Departement']}<br/>{row['Mandat']} : {row['Civilite']} {row['Prenom']} {row['Nom']}"
        else:
            print(f"!!! KO 'régional/outre-mer',... : {', '.join(row)}")
            n_reg_ko = n_reg_ko + 1
            continue


    elif 'Parlement européen' in row['Mandat']:
        # Parlement européen, Luxembourg
        coords = [49.6224195501072+offset[0], 6.146081355070288+offset[1]] 
        info = f"{row['Circonscription']}/{row['Departement']}<br/>{row['Mandat']} : {row['Civilite']} {row['Prenom']} {row['Nom']}"

    else:
        n_autre_ko = n_autre_ko + 1
        print(f"!!! TODO : {', '.join(row)}")
        continue
    # Ajout de l'item
    # ['Civilite', 'Nom', 'Prenom', 'Mandat', 'Circonscription', 'Departement',
    #  'Candidat', 'DatePublication']

    # Vérif coords : si NaN
    if  any(np.isnan(coords)):
        print(f"!! coords KO (->Paris) : {', '.join(row)}")
        coords = [48.856729+offset[0],2.291466+offset[1]]
    
        # if 'Paris' in row["Mandat"]:
        #     print(f"!! coords KO (->Paris) : {', '.join(row)}")
        #     offset = (0.5-random())*1e-2
        #     coords = [48.856729+offset,2.291466+offset]
        # elif 'Lyon' in row['Mandat']:
        # elif 'Lyon' in row['Mandat']:

    item = {"status": "Parrains",
    "candidat": row['Candidat'],
    "coordinates" : coords,
    "couleur": l_couleurs[row['Candidat']] if row['Candidat'] in l_couleurs.keys() else "lightgray",
    "infos": f"{info}<br /> -> {row['Candidat']}"
    }
    data_sites.append(item)

print(f"{len(data_sites)} parrains trouvés sur {len(df_parains)}")
print(f" # KO : communes {n_com_ko}, arrondissement {n_arrond_ko}, région {n_reg_ko}, département {n_dep_ko}, députés {n_deput_ko}, autres {n_autre_ko}")


#%% Sauvegarde en JSON 
with open('carto_parrains.json', 'w') as fp:
    json.dump(data_sites, fp)

# Fichier utilisé dynamiquement par index.html

#%% Création de la carte : inutile avec index.html
m = folium.Map(location=[46.7687714,4.5660859], 
    zoom_start=6.21, 
    max_zoom=18, min_zoom=1,
    tiles='OpenStreetMap', id = 'my_map')

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
m.save("index_old.html")

# %%
