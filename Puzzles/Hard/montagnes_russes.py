"""
https://www.codingame.com/training/hard/roller-coaster

File
Programmation dynamique
Simulation

Objectif
Vous venez d'être affecté au centre d'analyse et de supervision d'un nouveau parc d'attraction. Votre mission est d'estimer chaque jour quelle vont être les recettes de la journée pour chaque manège. Vous commencez par vous intéresser aux montagnes russes.
        Règles
Vous remarquez que les montagnes russes plaisent tellement aux gens que dès qu'ils ont fini un tour de manège, ils ne peuvent s’empêcher de revenir pour un nouveau tour.
Les personnes viennent faire la queue devant l'attraction.
Elles peuvent soit être seules, soit être en groupe. Lorsque des groupes sont dans la queue, ils veulent forcément monter ensemble à bord, sans être séparés.
Les personnes ne se doublent jamais dans la file d'attente.
Dès qu'il n'y a plus assez de place dans l'attraction pour le prochain groupe dans la queue, le manège démarre. (Il n'est donc pas toujours plein).
Dès que le tour de manège est terminé, les groupes qui en sortent retournent dans la file d'attente dans le même ordre.
Le manège contient un nombre L limite de places.
Le manège ne peut fonctionner que C fois dans une journée.
La file d'attente contient un nombre N de groupes.
Chaque groupe comporte un nombre Pi de personnes.
Chaque personne dépense 1 dirham par tour de manège.

        Exemples
Avec L=3, C=3 et 4 groupes (N=4) de tailles [3,1,1,2]:

Tour 1 : pour le premier tour de manège, seul le premier groupe peut monter et prend toutes les places. À la fin du tour, ce groupe retourne en fin de queue qui ressemble maintenant à [1,1,2,3].
Gain du tour : 3 dirhams.

Tour 2 : au second tour, les 2 groupes de 1 personnes suivantes peuvent monter, laissant une place vide (le groupe de 2 personnes qui les suit ne peut pas se séparer). À la fin du tour, ils retournent en fin de file : [2,3,1,1].
Gain du tour : 2 dirhams.

Tour 3 : pour le dernier tour (C=3), seul le groupe de 2 personnes peut entrer, laissant une place vide.
Gain du tour : 2 dirhams.

Gain total : 3+2+2 = 7 dirhams

        Entrées du jeu
Entrée
Ligne 1 : Les entiers L, C et N séparés par un espace.

N lignes suivantes : Chaque ligne contient un entier Pi correspondant au nombre de personnes dans un groupe. Les lignes sont ordonnées comme dans la file d'attente. (Les premières lignes correspondent aux premiers groupes pouvant monter).

Sortie
Un entier correspondant au nombre de dirham gagnés en fin de journée grâce aux montagnes russes (après C tours de manèges)

Contraintes
Pi ≤ L
1 ≤ L ≤ 10^7
1 ≤ C ≤ 10^7
1 ≤ N ≤ 1000
1 ≤ Pi ≤ 10^6

Exemples

Entrée
3 3 4
3
1
1
2
Sortie
7

Entrée
5 3 4
2
3
5
4
Sortie
14

Entrée
10 100 1
1
Sortie
100

"""

# code pour tester le script hors site
inputs = [
    "5 3 4",
    "2",
    "3",
    "5",
    "4",
]

output = 14

generator = (input for input in inputs)


def input():
    return next(generator)


######################################

from functools import lru_cache

l, c, n = [int(i) for i in input().split()]
queue = [
    int(input()) for _ in range(n)
]  # liste des groupes (valeur = nb de personnes dans le groupe)


@lru_cache(maxsize=None)  # dynamic programming with memoizing
def tour_type(
    index,
) -> tuple[
    int, int
]:  # pour un index de départ, calcule la recette et l'index à la fin du tour pour un tour
    recette = 0
    for _ in range(n):  # boucle sur chaque groupe
        recette += queue[index]  # 1 dirham par personne * nb de personnes
        if index == n - 1:  # si on est arrivée au bout de la queue, on revient au début
            index = 0
        else:
            index += 1  # sinon on passe au groupe suivant
        if recette + queue[index] > l:
            break  # on arrête si le groupe suivant ne peut pas monter
    return recette, index


recettes = 0
index = 0

for tour in range(c):  # boucle sur les c tours
    recette, index = tour_type(
        index
    )  # on calcule (ou récupère si déjà calculé !) la recette et la position du groupe à la fin du tour
    recettes += recette

print(recettes)
