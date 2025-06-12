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

# output = 2


generator = (input for input in inputs)  # type: ignore


def input():
    return next(generator)


########################################################################################################################################


from sys import stderr  # noqa: E402
from time import time  # noqa: E402
from functools import lru_cache  # noqa: E402
from collections import Counter  # noqa: E402

start_time = time()

DEBUG_MODE = 1  # 1 to view debug messages returned by eprint function, else 0


def eprint(*args, **kwargs):
    try:
        if DEBUG_MODE:
            print(*args, file=stderr, flush=True, **kwargs)
    except Exception as e:
        print("[EPRINT ERROR]", e, file=stderr, flush=True)


morse = {
    ".": "E",
    "-": "T",
    "..": "I",
    ".-": "A",
    "-.": "N",
    "--": "M",
    "...": "S",
    "..-": "U",
    ".-.": "R",
    ".--": "W",
    "-..": "D",
    "-.-": "K",
    "--.": "G",
    "---": "O",
    "....": "H",
    "...-": "V",
    "..-.": "F",
    ".-..": "L",
    ".--.": "P",
    ".---": "J",
    "-...": "B",
    "-..-": "X",
    "-.-.": "C",
    "-.--": "Y",
    "--..": "Z",
    "--.-": "Q",
}


inv_morse = {value: key for key, value in list(morse.items())}

sequence = input()
n = int(input())
words = [input() for _ in range(n)]

sequence_length = len(sequence)


# compute tous les code morse des mots du dictionnaire
def get_morse(word):
    morse = ""
    for letter in word:
        morse += inv_morse[letter]
    return morse


morses = []
for word in words:
    morses.append(get_morse(word))

# compute les morse identiques

morses_counter = Counter(morses)
unique_morses = [key for key in list(morses_counter.keys())]
get_morse_count_by_idx = [
    value for value in list(morses_counter.values())
]  # list faster than dict to map morse -> count by idx

# et leur longueur
get_morse_length_by_idx = [len(morse) for morse in unique_morses]

morse_max_length = max(get_morse_length_by_idx)

eprint("sequence=", sequence)
eprint("length=", sequence_length)
eprint("words=", words)
eprint("morses=", morses)
eprint("counter=", morses_counter)
eprint("max_length=", morse_max_length)


@lru_cache(maxsize=None)
def DP_recursive_decode(index: int) -> int:
    """
    recursively find the number of different messages you can decode from the beginning of the sequence
    returns sequence, and for all nodes : index after decode, score

    Args:
        index (int): position in the sequence to start decoding
        score (int): 1 per end_of_sequence_leaf (ie 1 unique message)
    """
    score = 0

    # end_of_sequence_leaf returns 1
    if index == sequence_length:
        # eprint(sequence, "ends at", index)
        return 1

    # parent returns sum of children score
    for idx, morse in enumerate(unique_morses):
        if sequence.startswith(morse, index):
            # eprint(sequence, "starts with", morse)
            score += get_morse_count_by_idx[idx] * DP_recursive_decode(
                index + len(morse)
            )

    return score


result = DP_recursive_decode(0)

print(result)

eprint("duration=", time() - start_time)
try:
    eprint(result == output)  # type: ignore
except Exception as e:
    print("[FINAL ERROR]", e, file=stderr, flush=True)


# best solutions:

# 1.memoization could be done without @lru_cache with a list like
# count = [0] * (sequence_length+1)
# count[0] = 1
# and computing iteratively from this list, index by index, the number of messages.

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

# the recursive function could use 'remainingcode' instead of index (performance to be checked...)
""" 
import functools
import sys
sys.setrecursionlimit(4000)
morse = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..'}

code = input()

ciphers = []
n = int(input())
for _ in range(n):
    word = input()
    ciphers.append(''.join([morse[letter] for letter in word]))

@functools.lru_cache()
def hunt(remainingcode):
    if len(remainingcode) == 0:
        return 1
    if not any(remainingcode.startswith(cipher) for cipher in ciphers):
        return 0
    return sum(hunt(remainingcode[len(cipher):]) for cipher in ciphers if remainingcode.startswith(cipher))

print(hunt(code))
"""
