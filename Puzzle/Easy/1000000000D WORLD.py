"""
https://www.codingame.com/training/easy/1000000000d-world

        Objectif
You are in 1000000000D World!
In 1000000000D World all vectors consist of exactly one billion integers.

People of 1000000000D World are quite smart and they know that due to low entropy and "curse of dimensionality" most of their billion-dimensional vectors have a lot of consequent repetitions. So they always store their vectors in a compressed form.

For example consider a vector in canonical form:

[1 1 1 2 2 3 3 3 3 3 3 3 3 3 3 3 3 3 3 ... (999999995 times 3)].

In compressed form it will become just:

[3 1 2 2 999999995 3] (which stands for 3 times 1 and 2 times 2 and 999999995 times 3).

Given two 1000000000D vectors A and B in compressed form, find the dot product of two vectors.

Dot product definition:
For two vectors a = [a_1 a_2 ... a_n] and b = [b_1 b_2 ... b_n] dot product "a • b" = a_1 * b_1 + a_2 * b_2 + ... + a_n * b_n

Entrée
Line 1: Compressed Vector A
Line 2: Compressed Vector B
Sortie
Dot product of A and B
Contraintes
The absolute values of the final result and all intermediate results are less than 2^40

Exemple
Entrée
500000001 1 499999999 -1
1000000000 1
Sortie
2

"""

# code pour tester le script hors site
entries = ["500000001 1 499999999 -1", "1000000000 1"]


generator = (entry for entry in entries)


def input():
    return next(generator)


######################################


a = list(map(int, input().split()))
b = list(map(int, input().split()))

i = j = result = 0

while i < len(a) and j < len(b):

    # n est la plus petite quantité de valeurs du 1er couple (quantité valeur) de a et b
    n = min(a[i], b[j])

    # dot product des n premières valeurs de a et b
    result += n * a[i + 1] * b[j + 1]

    # on retranche n à la 1ère quantité
    a[i] -= n
    b[j] -= n

    # si la 1ère quantité = 0, on passe à la suivante (indice += 2)
    i += 2 * (a[i] == 0)
    j += 2 * (b[j] == 0)

print(result)
