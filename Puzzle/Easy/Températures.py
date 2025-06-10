"""
https://www.codingame.com/training/easy/temperatures

Dans cet exercice, vous devez analyser un relevé de températures pour trouver quelle température se rapproche le plus de zéro.


Exemple de températures
Ici, -1 est le plus proche de 0.
        Règles
Écrivez un programme qui affiche la température la plus proche de 0 parmi les données d'entrée. Si deux nombres sont aussi proches de zéro, alors l'entier positif sera considéré comme étant le plus proche de zéro (par exemple, si les températures sont -5 et 5, alors afficher 5).
        Entrées du jeu
Votre programme doit lire les données depuis l'entrée standard et écrire le résultat sur la sortie standard.
Entrée
Ligne 1 : Le nombre N de températures à analyser.

Ligne 2 : Une chaine de caractères contenant les N températures exprimées sous la forme de nombres entiers allant de -273 à 5526

Sortie
Affichez 0 (zéro) si aucune température n'est fournie. Sinon, affichez la température la plus proche de 0
Contraintes
0 ≤ N < 10000
Exemple
Entrée
5
1 -2 -8 4 5
Sortie
1
"""

# code pour tester le script hors site
entries = [
    "5",
    "1 -2 -8 4 5",
]

generator = (entry for entry in entries)


def input():
    return next(generator)


######################################


n = int(input())
temperatures = input().split()
abs_temp_temp = []

for temp in temperatures:

    temp = int(temp)
    abs_temp_temp.append([abs(temp), temp])

abs_temp_temp = sorted(abs_temp_temp)

if n == 0:
    # "Affichez 0 (zéro) si aucune température n'est fournie."
    print(0)
elif n == 1:
    print(temperatures[0])
else:
    # "Si deux nombres sont aussi proches de zéro, alors l'entier positif sera considéré comme étant le plus proche de zéro"
    if abs_temp_temp[0][1] == -abs_temp_temp[1][1]:
        result = abs(abs_temp_temp[0][1])
    else:
        result = abs_temp_temp[0][1]

    print(result)
