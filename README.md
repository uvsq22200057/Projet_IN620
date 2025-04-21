# :bar_chart: Projet_IN620
Projet réalisé dans le cadre de l'UE Modèles de calcul &amp; Complexité IN620, de la L3 Informatique à l'UVSQ. Le but de ce projet est de simuler des automates cellulaires à une dimension et de s’en servir pour simuler une machine de Turing.


Les consignes sont données dans le [PDF consignes DM](automate.txt)

## :hammer_and_wrench: Makefile

Le projet inclut un fichier `Makefile` pour faciliter la compilation et l'exécution. Voici les principales commandes disponibles :

- `make`: Compile le projet.
- `make clean`: Supprime les fichiers compilés.
- `make zip` : Crée une archive ZIP du projet.
- `make run`: Compile et exécute le projet.

Assurez-vous d'avoir `make` installé sur votre système pour utiliser ces commandes.

## :office: Structure de données

### La cellule

Une cellule est représentée par une structure contenant son état `0 ou 1`. Nous y retrouvons également ses voisins, `left` et `right`qui sont des `pointeurs` vers d'autres cellule.
### L'automate cellulaire

L'automate cellulaire est modélisé comme une liste de cellules `[cell0, cell1, cell2, ...]`. 

Il possède également des règles de transition stockées dans un dictionnaire de la forme `{(state_left, state_center, state_right): state_next, ...}` qui définit l'évolution de chaque cellule en fonction de ses voisines.

### La configuration

La configuration correspond à l’état global de l’automate à un instant donné, c’est-à-dire la liste des états de toutes les cellules. Elle peut être affichée pour visualiser l’évolution de l’automate.

## :rocket: Fonctionnalités principales

- Simulation d’automates cellulaires à une dimension (ex : règle 110).
- Initialisation de la configuration à partir d'une chaine de `0 et de 1`.
- Affichage de l’évolution de l’automate sur plusieurs générations.
- Simulation d’une machine de Turing à un ruban à l’aide de l’automate cellulaire.

## :busts_in_silhouette: Auteurs

- GAUTEUR Mathilde :woman_student:
- CRAMETTE Noé :student:

**Date de rendu :** 4 mai 2025  

## :scroll: Licence 

Ce projet est distribué sous licence MIT.