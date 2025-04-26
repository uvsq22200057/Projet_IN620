# Projet_IN620
Projet réalisé dans le cadre de l'UE Modèles de calcul &amp; Complexité IN620, de la L3 Informatique à l'UVSQ. Le but de ce projet est de simuler des automates cellulaires à une dimension et de s’en servir pour simuler une machine de Turing.


Les consignes sont données dans le [PDF consignes DM](IN620_DM_2025.pdf)

## Makefile

Le projet inclut un fichier `Makefile` pour faciliter la compilation et l'exécution. Voici les principales commandes disponibles :

- `make`: Compile le projet.
- `make clean`: Supprime les fichiers compilés.
- `make zip` : Crée une archive ZIP du projet.
- `make run`: Compile et exécute le projet.

### Choix du modèle de calcul

Lorsque vous exécutez `make` dans un terminal, le programme vous demandera de choisir le modèle de calcul à simuler :

- **`0` : Automate cellulaire**
    - Avant de lancer la simulation, vous devrez spécifier le fichier sur lequel elle doit s’exécuter. Le programme affichera une liste des fichiers disponibles pour vous aider à faire votre choix.
    - Vous pourrez également configurer les paramètres de simulation suivants :
        - **Nombre maximal d’étapes** : Définissez une limite pour le nombre d’itérations de la simulation.
        - **Arrêt sur transition spécifique** : La simulation s’arrêtera si une transition particulière est rencontrée.
        - **Arrêt sur configuration stable** : La simulation s’arrêtera automatiquement si aucune modification d’état n’est détectée entre deux étapes consécutives.
- **`1` : Machine de Turing**
    - Avant de lancer la simulation, vous devrez spécifier le fichier sur lequel elle doit s’exécuter. Le programme affichera une liste des fichiers disponibles pour vous aider à faire votre choix.
    - Lance la simulation d’une machine de Turing.

Ce choix permet de basculer facilement entre les deux modèles en fonction des besoins de l’utilisateur.

Assurez-vous d'avoir `make` installé sur votre système pour utiliser ces commandes.

## Automate cellulaire

### La cellule

Une cellule est représentée par un entier `integer` correspondant à son état. Par convention, les bords du mot sont généralement fixés à `-1`, tandis que les cellules internes peuvent prendre n’importe quelle valeur entière positive, comprise entre `1 et l’infini`.

Un mot représentant une configuration est modélisé sous forme d’une liste de cellules encadrée par les bords, par exemple : `[-1, 0, 1, 0, ..., -1]`.

### L'automate cellulaire

L’automate cellulaire fonctionne à partir d’un ensemble de règles de transition, définies sous forme d’un `dictionnaire` Python.

Chaque règle est associée à une clé constituée d’un triplet `state_left, state_center, state_right` correspondant aux états de la cellule et de ses voisines gauche et droite. La valeur associée indique l’état que prendra la cellule au tour suivant. `{(state_left, state_center, state_right): state_next, ...}`.

Pour permettre une grande flexibilité et éviter de contraindre la structure du mot, l’état des bords est précisé à l’initialisation via le paramètre `default_state`. Cette valeur est utilisée pour les cellules situées aux extrémités du mot et qui n’ont pas de voisine.

### Configuration d'un automate

La configuration d’un automate cellulaire correspond à l’état global de celui-ci à un instant donné, c’est-à-dire la liste des états de toutes les cellules.

La méthode `next_step` permet de calculer la configuration suivante de l’automate. Elle retourne trois éléments :

- la nouvelle liste d’états,
- un booléen indiquant si la configuration a changé par rapport à l’étape précédente,
- la liste des transitions effectivement utilisées (si elles existent dans la table de règles).

Grâce à la fonction `simulate_automaton`, il est possible de simuler l’évolution d’un automate sur plusieurs générations. Cette fonction utilise `next_step`. Cette fonction accepte plusieurs paramètres utiles :

- le nombre maximal d’étapes à simuler (par défaut : 1000),
- une transition particulière à surveiller, qui peut stopper la simulation si elle est rencontrée,
- un arrêt anticipé si la configuration devient stable (aucun changement d’état entre deux étapes consécutives).

Chaque étape est affichée dans le terminal, ce qui permet de suivre visuellement l’évolution de la configuration au fil du temps.

### Fonctionnement

- Simulation d’automates cellulaires à une dimension (ex : règle 110).
- Initialisation de la configuration à partir d'une chaine de `0 et de 1`.
- Affichage de l’évolution de l’automate sur plusieurs générations.
- Simulation d’une machine de Turing à un ruban à l’aide de l’automate cellulaire.

## Machine de Turing

Le but est de simuler une machine de Turing de la même manière que pour un automate cellulaire. Les machines de Turing sont sur l'alphabet de travail ``

## Auteurs

- GAUTEUR Mathilde
- CRAMETTE Noé

**Date de rendu :** 4 mai 2025  

## Licence 

Ce projet est distribué sous licence MIT.