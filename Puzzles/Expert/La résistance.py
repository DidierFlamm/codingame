"""
https://www.codingame.com/training/expert/the-resistance

Opportunités d'apprentissage

Mémoïsation
Programmation dynamique
Récursion
Encodage

Objectif
Vous travaillez au musée de la Résistance nationale et vous venez d'exhumer des centaines de documents contenant des transmissions codées en Morse. Dans les documents, aucun espace n'a été retranscrit pour séparer les lettres et les mots qui se cachent derrière une séquence en Morse. Une séquence décodée peut donc avoir différentes interprétations.

Votre programme devra déterminer le nombre de messages différents qu'il est possible d'obtenir à partir d'une séquence en Morse et d'un dictionnaire donné.
        Règles
Le Morse est un codage composé de points et de traits représentant des lettres de l'alphabet. Voici la transcription d'un alphabet en Morse :
 A  .-	 B  -...	 C  -.-.	 D  -..
 E  .	 F  ..-.	 G  --.	 H  ....
 I  ..	 J  .---	 K  -.-	 L  .-..
 M  --	 N  -.	 O  ---	 P  .--.
 Q  --.-	 R  .-.	 S  ...	 T  -
 U  ..-	 V  ...-	 W  .--	 X  -..-
 Y  -.--	 Z  --..

Puisqu'aucun des espaces n'ont été retranscrits, plusieurs interprétations des messages sont possibles. Par exemple, la séquence -....--.-. peut aussi bien correspondre à BAC, BANN, DUC, DU TETE, ....

Un être humain est capable de reconnaître le découpage adéquat grâce à sa connaissance de la langue mais pour une machine c'est plus délicat. Pour que votre programme puisse faire l'équivalent vous avez à votre disposition un dictionnaire contenant un ensemble de mots corrects.

Cependant, même avec un dictionnaire, il est possible qu'une séquence puisse correspondre à plusieurs messages valides (BAC, DUC, DU et TETE pourraient être présents dans le dictionnaire de l'exemple précédent).

Source : ACM Contest Problems Archive


        Entrées du jeu
Entrée
Ligne 1 : une séquence Morse de longueur maximale L

Ligne 2 : un entier N correspondant au nombre de mots du dictionnaire

Les N Lignes suivantes : un mot du dictionnaire par ligne. Chaque mot a une longueur maximale M et n’apparaît qu'une seule fois dans le dictionnaire.



Sortie
Un entier R correspondant au nombre de messages qu'il est possible de générer à partir de la séquence en Morse et du dictionnaire.
Contraintes
0 < L < 100000

0 < N < 100000

0 < M < 20

0 ≤ R < 2^63

Exemple

Entrée
......-...-..---.-----.-..-..-..
5
HELL
HELLO
OWORLD
WORLD
TEST

Sortie
2
"""

inputs = [
    "......-...-..---.-----.-..-..-..",
    "5",
    "HELL",
    "HELLO",
    "OWORLD",
    "WORLD",
    "TEST",
]

# example test

output = 2

inputs = ["..............................................", "2", "E", "I"]

# last CG test

output = 2971215073

generator = (input for input in inputs)  # type: ignore


def input():
    return next(generator)


######################################################################
# do not copy paste code above this line in CG IDE                   #
#######################################################################################################################################
# copy paste this cell in CG IDE if you want to evaluate performance #
######################################################################

from sys import stderr  # noqa: E402
from time import time  # noqa: E402

start_time = time()

DEBUG_MODE = 1  # 1 to view debug messages returned by eprint function, else 0


def eprint(*args, **kwargs):
    try:
        if DEBUG_MODE:
            print(*args, file=stderr, flush=True, **kwargs)
    except Exception as e:
        print("[EPRINT ERROR]", e, file=stderr, flush=True)


from time import perf_counter  # noqa: E402
from statistics import mean, stdev  # noqa: E402

start_time = perf_counter()

########################################################################################################################################
# copy paste this cell in CG IDE #
##################################
from functools import lru_cache  # noqa: E402
from collections import Counter  # noqa: E402

sequence = input()
n = int(input())
words = [input() for _ in range(n)]

morse_dict = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
}


def encrypt(word):
    cipher = ""
    for letter in word:
        cipher += morse_dict[letter]
    return cipher


def encrypt_iterable(words):
    ciphers = []
    for word in words:
        ciphers.append(encrypt(word))
    # returns tuple because memoization needs immutable variables for hashing
    return tuple(ciphers)


def get_unique_ciphers_and_counts(ciphers):
    cipher_counter = Counter(ciphers)
    unique_ciphers = tuple(key for key in list(cipher_counter.keys()))
    unique_cipher_counts = tuple(
        value for value in list(cipher_counter.values())
    )  # ciphers are counted because different words may have the same cipher
    return unique_ciphers, unique_cipher_counts


@lru_cache(maxsize=None)
def DP_recursive_decode(index: int) -> int:
    """
    Recursively computes the total number of distinct decoding paths
    of a Morse code sequence starting from a given index.

    This implementation uses top-down dynamic programming (DP) with memoization
    (via functools.lru_cache) to avoid redundant calculations.

    Args:
        index (int): Current position in the sequence to decode from.

    Returns:
        int: The total number of valid decoding paths from this index.
             Each complete decoding path contributes 1.
             Intermediate positions sum the scores of their children.
    """
    total_decodings = 0

    # Base case: reached end of the sequence, count as 1 valid decoding
    if index == sequence_length:
        return 1

    # Explore all unique ciphers matching the sequence at the current index
    for idx, cipher in enumerate(unique_ciphers):
        if sequence.startswith(cipher, index):  # startswith is already optimized in C
            total_decodings += unique_cipher_counts[idx] * DP_recursive_decode(
                index + len(cipher)
            )
    return total_decodings


sequence_length = len(sequence)
ciphers = encrypt_iterable(words)
unique_ciphers, unique_cipher_counts = get_unique_ciphers_and_counts(ciphers)

result = DP_recursive_decode(0)

print(result)

###############################################################################################################################
# copy paste this cell in CG IDE if you want to evaluate performance #
######################################################################

end_time = perf_counter()

try:
    eprint(
        ("✅" if result == output else "❌") + " result is",
        result == output,
        f"(got {result}, expected {output})",
    )
except Exception as e:
    print("[FINAL ERROR]", e, file=stderr, flush=True)

eprint("\n          sequence:", sequence)
eprint("   sequence length:", sequence_length)
eprint("             words:", words)
eprint("unique morse codes:", unique_ciphers)
eprint("            counts:", unique_cipher_counts)

eprint(f"\n{DP_recursive_decode.cache_info()}")
duration_us = (end_time - start_time) * 1e6
eprint(f"\n        script duration: {duration_us:.3f} µs")

number = (
    100  # test 4 will run out time and fail if you compute mean with 100 iterations
)
durations = []
for _ in range(number):
    DP_recursive_decode.cache_clear()
    start_time = perf_counter()
    DP_recursive_decode(0)
    end_time = perf_counter()
    durations.append(end_time - start_time)

durations_us = [d * 1e6 for d in durations]

eprint(
    f" mean function duration: {mean(durations_us):.3f} µs (over {number} calls of the recursive function)"
)
eprint(f"                    std: {stdev(durations_us):.3f} µs")

eprint(
    f"duration of script head: {duration_us-mean(durations_us):.3f} µs (ie script duration - mean function duration)"
)

##################################################################################################################################

#######################################################################################################
# Piste d'optimisation: remplacer la récursion + lru_cache par une programmation dynamique itérative: #
#   Créer un tableau count de taille len(sequence)+1,                                                 #
#   count[0] = 1 (une façon de dire qu’on a 1 façon de décoder la séquence vide),                     #
#   Parcourir la séquence en testant les mots en morse à chaque position, et accumuler les décomptes. #
#   C’est souvent plus rapide et ne pose pas problème de limite de récursion.                         #
#######################################################################################################

# 2 examples from CG board:

"""
morse = {
'A': '.-',  'B': '-...','C': '-.-.','D': '-..', 'E': '.',  'F': '..-.','G': '--.', 'H': '....','I': '..',
'J': '.---','K': '-.-', 'L': '.-..','M': '--',  'N': '-.', 'O': '---', 'P': '.--.','Q': '--.-','R': '.-.',
'S': '...', 'T': '-',   'U': '..-', 'V': '...-','W': '.--','X': '-..-','Y': '-.--','Z': '--..'}

message = input()
words = ["".join(morse[letter] for letter in input()) for _ in range(int(input()))]
    
counter = [0]*(len(message)+1)
counter[0]=1

for position, count in enumerate(counter):
    if count:
        for word in words:
            if message.startswith(word, position):
                counter[position + len(word)] += count
                
print(counter[-1])
"""

#########################################################################################

"""
import sys
import math

code = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
     	'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..'
}

morsetext = input()
n = int(input())
morselen = len(morsetext)

#create morse wordlist (list)
wordlist = [""] * n
for i in range(n):
    word=input()
    for char in word:
        wordlist[i] += code[char]

wordset=set(wordlist)  #much faster to search, but doesn't contain duplicates

maxlen = len(max(wordset, key=len)) 
minlen = len(min(wordset, key=len)) 

#memoization
count = [0] * (morselen+1)
count[0] = 1

for end in range(1,morselen+1):
    for seglength in range(minlen, min(maxlen,end)+1 ):
        segment = morsetext[end-seglength:end]
        if segment in wordset :
            count[end] += count[end-seglength] * wordlist.count(segment)

print(count[-1]) 
"""
