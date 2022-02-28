# parrainages-communes-2022
Une visualisation des parrainages par commune : au 28/02/2022, 10254 parrains cortagraphiés sur 10265.

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
!!! KO 'métropolitain',... : Mme, PÉTRUS, Annick, Sénatrice, , Saint-Martin, PÉCRESSE Valérie, 2022-02-08T00:00:00, , SAINT MARTIN
!!! KO 'régional/outre-mer',... : M., GIBBS, Daniel, Membre d'une assemblée d'une collectivité territoriale d'outre-mer à statut particulier, , Saint-Martin, PÉCRESSE Valérie, 2022-02-15T00:00:00, , SAINT MARTIN
!!! KO 'régional/outre-mer',... : M., MATIGNON, Francius, Membre d'une assemblée d'une collectivité territoriale d'outre-mer à statut particulier, , Saint-Barthélemy, PÉCRESSE Valérie, 2022-02-17T00:00:00, , SAINT BARTHELEMY
!!! KO 'régional/outre-mer',... : M., GROS-DESORMEAUX, Hary, Membre d'une assemblée d'une collectivité territoriale d'outre-mer à statut particulier, , Saint-Martin, PÉCRESSE Valérie, 2022-02-17T00:00:00, , SAINT MARTIN
!!! KO 'régional/outre-mer',... : M., BORDJEL, Patrick, Membre d'une assemblée d'une collectivité territoriale d'outre-mer à statut particulier, , Saint-Barthélemy, ZEMMOUR Éric, 2022-02-17T00:00:00, , SAINT BARTHELEMY
!!! KO 'régional/outre-mer',... : M., MAGRAS, Bruno, Membre d'une assemblée d'une collectivité territoriale d'outre-mer à statut particulier, , Saint-Barthélemy, ZEMMOUR Éric, 2022-02-17T00:00:00, , SAINT BARTHELEMY
!!! TODO : M., LUCCHINI, Jean-Jacques, Membre de l'Assemblée de Corse, , Corse-du-Sud, JADOT Yannick, 2022-02-22T00:00:00, , CORSE DU SUD
!!! TODO : Mme, NIVAGGIONI, Nadine, Membre de l'Assemblée de Corse, , Corse-du-Sud, JADOT Yannick, 2022-02-22T00:00:00, , CORSE DU SUD
!!! TODO : Mme, PEDINIELLI, Chantal, Membre de l'Assemblée de Corse, , Corse-du-Sud, PÉCRESSE Valérie, 2022-02-22T00:00:00, , CORSE DU SUD
!!! TODO : M., BICCHIERAY, Didier, Membre de l'Assemblée de Corse, , Haute-Corse, PÉCRESSE Valérie, 2022-02-22T00:00:00, , HAUTE CORSE
!!! KO 'métropolitain',... : Mme, GUION-FIRMIN, Claire, Députée, 1ère circonscription, Saint-Martin / Saint-Barthélémy, PÉCRESSE Valérie, 2022-02-22T00:00:00, 1ERE CIRCONSCRIPTION, SAINT MARTIN / SAINT BARTHELEMY
!! coords KO (->Paris) : Mme, FELEU, Yannick, Membre d'une assemblée d'une collectivité territoriale d'outre-mer à statut particulier, , Wallis et Futuna, PÉCRESSE Valérie, 2022-02-24T00:00:00, , WALLIS ET FUTUNA
10254 parrains trouvés sur 10265
 # KO : communes 0, arrondissement 0, région 5, département 0, députés 2, autres 4
```

Auteur : Gilles Gonon
