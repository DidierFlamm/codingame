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

output = 2

inputs = ["..............................................", "2", "E", "I"]

output = 2971215073

generator = (input for input in inputs)  # type: ignore


def input():
    return next(generator)


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


from functools import lru_cache  # noqa: E402
from collections import Counter  # noqa: E402


morse_dict = {
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

inv_morse_dict = {value: key for key, value in list(morse_dict.items())}

# inputs
sequence = input()
n = int(input())
words = [input() for _ in range(n)]


# function computing tuple of morse codes of each word from an iterable
def get_morse_codes(words):

    # sub-function computing morse code from word
    def get_morse_from_word(word):
        morse_code = ""
        for letter in word:
            morse_code += inv_morse_dict[letter]
        return morse_code

    morse_codes = []
    for word in words:
        morse_codes.append(get_morse_from_word(word))

    morse_codes = tuple(
        morse_codes
    )  # memoization needs hashable variables (ie immutable)
    return morse_codes


# function computing unique morse codes from an iterable, their count and length


def get_unique_morse_codes_and_counts(morse_codes):
    morses_counter = Counter(morse_codes)
    unique_morse_codes = tuple(key for key in list(morses_counter.keys()))
    unique_morse_code_counts = tuple(
        value for value in list(morses_counter.values())
    )  # counts are necessary because different words may have same morse codes
    # unique_morse_codes_length = tuple(len(morse) for morse in unique_morse_codes)
    return unique_morse_codes, unique_morse_code_counts  # , unique_morse_codes_length


# recursive function to compute number of different messages from a sequence
# using Dynamic Programming and Memoization


@lru_cache(maxsize=None)
def DP_recursive_decode(
    # sequence: str,
    # sequence_length: int,
    # unique_morse_codes: tuple,
    # unique_morse_code_counts: tuple,
    index: int,
) -> int:
    """
    Recursively compute the number of different messages you can decode from the sequence starting from the given index
    Returns:
        score (int): score = 1 per unique message (ie number of end-of-sequence-leaves), else 0 (ie intermediate nodes or non-end-of-sequence-leaf)
    """
    score = 0

    # end_of_sequence_leaf returns 1
    if index == sequence_length:
        return 1

    # parent returns sum of children score
    for idx, morse in enumerate(unique_morse_codes):
        if sequence.startswith(morse, index):  # startswith is already optimized in C
            score += unique_morse_codes_count[idx] * DP_recursive_decode(
                # sequence,
                # sequence_length,
                # unique_morse_codes,
                # unique_morse_code_counts,
                index
                + len(morse),
            )

    return score


sequence_length = len(sequence)
unique_morse_codes, unique_morse_codes_count = get_unique_morse_codes_and_counts(words)


result = DP_recursive_decode(
    # sequence, sequence_length, unique_morse_codes, unique_morse_codes_count,
    0
)

print(result)


###############################################################################################################################

end_time = perf_counter()

try:
    eprint(("✅" if result == output else "❌") + " result is", result == output)
except Exception as e:
    print("[FINAL ERROR]", e, file=stderr, flush=True)


eprint("\ncache info after one call:", DP_recursive_decode.cache_info())
duration = end_time - start_time
eprint("\nscript duration:", int(duration * 1e6), "µs")
number = 1000
durations = []

for _ in range(number):
    start_time = perf_counter()
    DP_recursive_decode(
        # sequence, len(sequence), unique_morse_codes, unique_morse_codes_count,
        0
    )
    end_time = perf_counter()
    # print(end_time - start_time)

    durations.append(end_time - start_time)
    DP_recursive_decode.cache_clear()
    # print("Cache info after clear:", DP_recursive_decode.cache_info())


durations_us = [d * 1e6 for d in durations]

print(
    f"  mean duration: {mean(durations_us):.3f} µs (over {number} iterations of recursive function only)"
)
print(f"            std: {stdev(durations_us):.3f} µs")

# best solutions:

# 1 and 2. memoization could be done without @lru_cache with a list like
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

# 3. the recursive function could use 'remainingcode' instead of index (performance to be checked...)
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
