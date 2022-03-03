# parrainages-communes-2022
Une visualisation des parrainages par commune, assemblée, collectivité, ... : au 03/03/2022, 12751 parrains cortagraphiés sur 12751 😅.

Cartographie à retrouver [en ligne ici](https://giloop.github.io/parrainages-communes-2022/)

![Carte des parrainages](https://giloop.github.io/parrainages-communes-2022/parrainages-2022.jpg)

Réalisation en Python : 

- script v1: `parrainage_com.py`  utilise la librairie Folium qui génère une page html statique. (index_old.html) 
- script v2: `parrainage_com_v2.py` réalise une localisation plus poussée des parrains et génère désormais un fichier json chargé dynamliquement depuis index.html.

Le code réalise principalement l'appariement des données et la génération de la carte avec les marqueurs géolocalisés des parrainages des différents candidats.

## Données utilisées

Les données ont été trouvé notamment grace à un article sur [datavis.fr](https://www.datavis.fr/) avec des [considérations intéressantes](https://www.datavis.fr/index.php?page=validate-your-data) sur la localisation des données.

- Données de parrainages du conseil constitutionnel, à retrouver [ici](https://presidentielle2022.conseil-constitutionnel.fr/les-parrainages/tous-les-parrainages-valides.html)
- Données INSEE de géolocalisation des communes de France, [ici](https://www.data.gouv.fr/fr/datasets/codes-insee-communes-g-olocalis-es/)
- Données la poste : liste de communes plus à jour avec localisation GPS, disponible [ici](https://datanova.legroupe.laposte.fr/explore/dataset/laposte_hexasmal/export/?disjunctive.code_commune_insee&disjunctive.nom_de_la_commune&disjunctive.code_postal&disjunctive.libell_d_acheminement&disjunctive.ligne_5)
- Données EU circonscription : utilisé définition des régions, départements.

Pas mal de coordonnées GPS ont été rajoutées à la main par mes soins. 

## Log de l'appariemment

```
12751 parrains trouvés sur 12751
 # KO : communes 0, arrondissement 0, région 0, département 0, députés 0, autres 0
```

Auteur : Gilles Gonon
