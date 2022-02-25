# parrainages-communes-2022

Visualisation à retrouver [ici](https://giloop.github.io/parrainages-communes-2022/)

![Carte des parrainages](https://giloop.github.io/parrainages-communes-2022/parrainages-2022.jpg)

Une visualisation des parrainages par communes. 
Réalisation en Python à l'aide de la librairie Folium qui génère une page html statique. 

Le code réalise principalement l'appariement des données et la génération de la carte avec les marqueurs des parrainages des différents candidats.

- Données de parrainages du conseil constitutionnel, à retrouver [ici](https://presidentielle2022.conseil-constitutionnel.fr/les-parrainages/tous-les-parrainages-valides.html)
- Données INSEE de géolocalisation des communes de France, [ici](https://www.data.gouv.fr/fr/datasets/codes-insee-communes-g-olocalis-es/)
- Données la poste : liste de communes plus à jour
- Données EU circonscription : utilisé définition des régions, départements

Autres sources de données d'intérêt :
- https://datanova.legroupe.laposte.fr/explore/dataset/laposte_hexasmal/export/?disjunctive.code_commune_insee&disjunctive.nom_de_la_commune&disjunctive.code_postal&disjunctive.libell_d_acheminement&disjunctive.ligne_5
- https://www.datavis.fr/index.php?page=validate-your-data : considération sur la localisation des communes françaises et source eucircos...



Auteur : Gilles Gonon
