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
    - Sélectionner un fichier parmi ceux disponibles dans le dossier automata/ (la liste vous sera affichée automatiquement).
    - Vous pourrez également configurer les paramètres de simulation suivants :
        - **Nombre maximal d’étapes** : définissez une limite pour le nombre d’itérations de la simulation.
        - **Arrêt sur transition spécifique** : la simulation s’arrêtera si une transition particulière est rencontrée.
        - **Arrêt sur configuration stable** : la simulation s’arrêtera automatiquement si aucune modification d’état n’est détectée entre deux étapes consécutives.
        - **Configuration initiale** : spécifiez l'état initial de l'automate cellulaire.

- **`1` : Machine de Turing**
    - Sélectionner un fichier dans le dossier turing/ (la liste vous sera proposée).
    - Indiquer le mot d’entrée à traiter par la machine.

- **`2` : Simulation d'un MT sur un automate**
    - Sélectionner un fichier dans le dossier turing/ (la liste vous sera proposée).
    - Indiquer le mot d’entrée à traiter par l'automate depuis le code d'une machine de Turing.

Ce choix permet de basculer facilement entre les deux modèles en fonction des besoins de l’utilisateur.

Assurez-vous d'avoir `make` installé sur votre système pour utiliser ces commandes.

## Automate cellulaire

### La cellule

Une cellule est représentée par un entier `integer` correspondant à son état. Par convention, les bords du mot sont généralement fixés à `-1`, tandis que les cellules internes peuvent prendre n’importe quelle valeur entière positive, comprise entre `0 et l’infini`.

Un mot représentant une configuration est modélisé sous forme d’une liste de cellules encadrée par les bords, par exemple : `[-1, 0, 1, 0, ..., -1]`.

### L'automate cellulaire

L’automate cellulaire fonctionne à partir d’un ensemble de règles de transition, définies sous forme d’un `dictionnaire` Python.

Chaque règle est associée à une clé constituée d’un triplet `state_left, state_center, state_right` correspondant aux états de la cellule et de ses voisines gauche et droite. La valeur associée indique l’état que prendra la cellule au tour suivant. `{(state_left, state_center, state_right): state_next, ...}`.

Pour permettre une grande flexibilité et éviter de contraindre la structure du mot, l’état des bords est précisé à l’initialisation via le paramètre `default_state`. Cette valeur est utilisée pour les cellules situées aux extrémités du mot et qui n’ont pas de voisine.

Egalement, l'automate cellulaire stocke l'`alphabet` de travail. Cette alphabet est utilisé pour vérifier la validité des états des cellules dans la simulation.	

### Configuration d'un automate

La configuration d’un automate cellulaire correspond à l’état global de celui-ci à un instant donné, c’est-à-dire la liste des états de toutes les cellules.

La méthode `next_step` permet de calculer la configuration suivante de l’automate. Elle retourne trois éléments :

- la nouvelle liste d’états,
- un booléen indiquant si la configuration a changé par rapport à l’étape précédente,
- la liste des transitions utilisées (si elles existent dans la table de règles).

Grâce à la fonction `simulate_automaton`, il est possible de simuler l’évolution d’un automate sur plusieurs générations. Cette fonction utilise `next_step`. Cette fonction accepte plusieurs paramètres utiles :

- le nombre maximal d’étapes à simuler (par défaut : 1000),
- une transition particulière à surveiller, qui peut stopper la simulation si elle est rencontrée,
- un arrêt anticipé si la configuration devient stable (aucun changement d’état entre deux étapes consécutives).

Chaque étape est affichée dans le terminal, ce qui permet de suivre visuellement l’évolution de la configuration au fil du temps.

### Exemples d'automates cellulaires
Voici quelques exemples d'automates cellulaires que vous pouvez simuler :

1. **_spread_** : Un automate qui fait grandir sa configuration a l’infini en propageant l’information sur ses bords. L'alphabet de travail est `0, 1` avec pour bords `-1`.

2. **_cycle_** : Un automate qui fait cycler les valeurs de ses cases. L'exemple travaille sur l'alphabet `0, 1, 2` avec pour bords `-1`. 0 => 1, 1 => 2, 2 => 0. Il est possible de le faire fonctionner sur d'autres alphabets en modifiant la table de transition.

3. **_eater_** : Un automate qui interdit d'avoir trois cellules consécutives de même état. L'exemple travaille sur l'alphabet `0, 1` avec pour bords `-1`.

4. **_runner_** et **_runner2_** : Deux automates cellulaires qui se déplacent sur la bande. Runner2 est une version améliorée de runner, capable de changer de direction en fonction de la valeur rencontrée. En mettant un `2` sur la bande, l'automate se déplace vers la gauche. En mettant un `1`, il se déplace vers la droite. Exemple : 1000 => 0100 => 0010 => 0002 => 0020 => 0200 => 1000 ...

5. **_rule_110_** : Un automate cellulaire à une dimension qui est connu pour être Turing-complet. Il fonctionne sur l'alphabet `0, 1` avec pour bords `-1`.

## Machine de Turing

Le but est de simuler une machine de Turing de la même manière que pour un automate cellulaire. Les machines de Turing sont sur l'alphabet de travail `0, 1` et sur l'alphabet de bande `0, 1, -`. Le symbole `-` est utilisé pour représenter une cellule vide sur la bande.

### La machine de Turing

Nous définissons une machine de Turing comme tel :
- **un ensemble de transitions** : une transition valide s'écrit comme tel : `état, symbole : nouvelle_état, nouveau_symbole, direction`. Exemple : `q0,0 : q1,1,R`
- **un état initial**
- **un état d'acceptation**
- **l'état de défaut de la bande** : permet de représenter une cellule vide

La première ligne d'un fichier contenant le code d'une machine de Turing représente l'état acceptant : exemple `accept qf`

La première ligne d'une transition représente l'état initial.

### Configuration d'une machine de Turing
La configuration d'une machine de Turing est représentée par une liste de cellules, où chaque cellule peut contenir un symbole de l'alphabet de bande. 

La tête de lecture/écriture est représentée par un entier indiquant la position actuelle sur la bande.

Nous y retrouvons également l'état courant de la machine de Turing.

La méthode `next_step` permet de calculer la configuration suivante de la machine de Turing.

Grâce à la fonction `simulate_turing`, il est possible de simuler l’évolution d’une machine de Turing sur plusieurs générations. Celle-ci s'arrête lorsque la machine de Turing atteint l'état d'acceptation ou lorsqu'aucune transition n'est possible.

### Exemples de machines de Turing
Voici quelques exemples de machines de Turing que vous pouvez simuler :
1. **_binary_addition_** : Une machine de Turing qui effectue l'addition binaire. Exemple : `000 => 001`, `001 => 010`, `010 => 011`, `011 => 100`, `100 => 101`, `101 => 110`, `110 => 111`, `111 => 1000`.
2. **_subtract_binary_** : Une machine de Turing qui soustrait 1 à un nombre binaire. Exemple : `000 => 111`, `001 => 000`, `010 => 001`, `011 => 010`, `100 => 011`, `101 => 100`, `110 => 101`, `111 => 110`.

## Simulation d'une machine de Turing sur un automate cellulaire

La simulation d'une machine de Turing sur un automate cellulaire est une extension de la simulation d'une machine de Turing classique. Dans ce cas, la machine de Turing est utilisée pour manipuler les états des cellules d'un automate cellulaire.

La machine de Turing agit sur la bande de l'automate cellulaire, en modifiant les états des cellules en fonction des transitions définies dans le code de la machine de Turing.

Afin de savoir où se trouve la tête de lecture/écriture de la machine de Turing, nous utilisons un état spécial `q00`, ici cela signifie que nous sommes sur la tête de lecture, sur l'état `q0` et avec un symbole `0`. 

Les autres symboles sont écris de la forme suivante : `*0`, `*1`, `*2`, etc. où `*` signifie que nous ne sommes pas sur la tête de lecture/écriture.

Les transitions de l'automate cellulaire simulé avec le code d'une machine de Turing reste un `dictionnaire`.

### Conversion de la machine de Turing en automate cellulaire
La conversion d'une machine de Turing en automate cellulaire est réalisée en utilisant un dictionnaire de transitions. Chaque transition de la machine de Turing est convertie en une règle de transition pour l'automate cellulaire.

La première ligne reste l'état initial de la machine de Turing. 

Ensuite, chaque transition est convertie en une règle de transition pour l'automate cellulaire. Par exemple, la transition `q0,0 : q1,1,R` donne `(*0,q10,*1) = (*1)` et `(q10,*1, *1) = (q21)`.

### La simulation

La simulation d'une machine de Turing sur un automate cellulaire est réalisée en utilisant la méthode `simulate_automaton`. Cette méthode simule l'évolution de l'automate cellulaire en appliquant les règles de transition définies par le code de la machine de Turing.

### Exemples de simulation
Voici quelques exemples de simulation d'une machine de Turing sur un automate cellulaire :
1. **_+1_en binaire_**
2. **_-1 en binaire_** 

## Auteurs

- GAUTEUR Mathilde
- CRAMETTE Noé

**Date de rendu :** 4 mai 2025  