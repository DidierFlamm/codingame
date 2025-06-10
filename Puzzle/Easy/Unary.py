"""
https://www.codingame.com/training/easy/unary

        Objectif
Le binaire avec des 0 et des 1 c'est bien. Mais le binaire avec que des 0, ou presque, c'est encore mieux.

Écrivez un programme qui, à partir d'un message en entrée, affiche le message codé avec cette technique en sortie.

        Règles
Voici le principe d'encodage :

Le message en entrée est constitué de caractères ASCII (7 bits)
Le message encodé en sortie est constitué de blocs de 0
Un bloc est séparé d'un autre bloc par un espace
Deux blocs consécutifs servent à produire une série de bits de même valeur (que des 1 ou que des 0) :
- Premier bloc : il vaut toujours 0 ou 00. S'il vaut 0 la série contient des 1, sinon elle contient des 0
- Deuxième bloc : le nombre de 0 dans ce bloc correspond au nombre de bits dans la série
        Exemple
Prenons un exemple simple avec un message constitué d'un seul caractère : C majuscule. C en binaire vaut 1000011 ce qui donne avec cette technique :

0 0 (la première série composée d'un seul 1)
00 0000 (la deuxième série composée de quatre 0)
0 00 (la troisième série composée de deux 1)
C vaut donc : 0 0 00 0000 0 00


Deuxième exemple, nous voulons encoder le message CC (soit les 14 bits 10000111000011) :

0 0 (un seul 1)
00 0000 (quatre 0)
0 000 (trois 1)
00 0000 (quatre 0)
0 00 (deux 1)
CC vaut donc : 0 0 00 0000 0 000 00 0000 0 00

        Entrées du jeu
Entrée
Ligne 1 : le message composé de N caractères ASCII (sans retour chariot)
Sortie
Le message encodé
Contraintes
0 < N < 100
Exemple
Entrée
C
Sortie
0 0 00 0000 0 00

"""

# code pour tester le script hors site
entries = ["C"]


generator = (entry for entry in entries)


def input():
    return next(generator)


######################################

from itertools import groupby

binary_message = ""
encoded_message = ""

message = input()

for letter in message:
    binary_message += f"{ord(letter):07b}"

grouped_bits_list = [list(grouped_bits) for _, grouped_bits in groupby(binary_message)]

for grouped_bits in grouped_bits_list:
    encoded_message += (
        ("0 " if int(grouped_bits[0]) else "00 ") + "0" * len(grouped_bits) + " "
    )

print(encoded_message[:-1])
