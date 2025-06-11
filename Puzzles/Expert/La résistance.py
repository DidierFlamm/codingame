"""
https://www.codingame.com/training/expert/the-resistance

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

"""
Tips pour récursif ! 
string[position:].startswith(short_string)
takes 10x more time then:

string.startswith(short_string, position)

"""

""" 
TRIE data structure
https://en.wikipedia.org/wiki/Trie
"""

""" 
I used DP using a trie as data store.
"""

""" 
At the end storing where each letter begins in the input string helped me for faster finding where each word from the dictionary begins. After that I used a recursion over the dictionary words and count how many words start at a given index of the input word and span to the end of the input string, that way I do not go through the how string every time.
"""
""" 
TIPS 1
Let’s say you’ve got a sequence of 1000 dots and dashes. One possible word ends at position 100, but other words are still possible on the same path (e.g. you’ve parsed out the word HELLO the words HELLO and HELLOWORLD are both in the dictionary). This is a fork; from position 100 you can start a new word (path B) or continue checking to see if HELLOWORLD is possible (path A).

Paths A and B both end somewhere. Let’s say they both end at the same spot, position 150 (e.g. the word WORLD is also in the dictionary). This is what I mean by the path reconverging; paths A and B both lead to new path C at position 150. When you get done parsing path A, you parse path C until you hit an endpoint, then go back to parse path B. Path B ends at the beginning of path C. However, since you already parsed path C once, you don’t need to do it again.

This kind of thing happens a lot in the larger tests, and the paths can split several times before recombining. You can waste a lot of compute cycles parsing out stuff you already did if you don’t take it into account.
"""

""" 
TIPS 2
Switching to a decent cache allowed me to use the simplest recursion and implied DFS, with the DP boosting performance to millisecond range

"""

""" 
TIPS 3
~34 ms in Python3 for the last test case. struggled a lot until i discovered identical sequences could be different words… simple recursion with memoization.
"""

""" 
TIPS 4
A few words on this one. I did a standard recursion with strings matching & memoization to avoid recursion on already-done paths.

"""

""" 
I used tries, as others did.
Some have mentioned that memoization was not necessary; but the way I did it, after the trie was built (based on all the words in the dictionary), I stepped through the message exactly once. For each bit in the message, I checked whether the current node in the trie had a branch for that bit. If it did, and if the next node had leaves in the trie, I multiplied the number of leaves by the previous leaves and spawned a new “thread” starting from the base of the trie on the next bit. Well, actually, for each bit, I totalled the number of leaves occurring from all the relevant nodes, and created one new search thread with that number. And if the node represented in that thread had a NULL pointer for that branch, I took the thread out of the list.
When I reached the last bit, instead of starting a new thread with that total number of leaves, I simply printed it.
I didn’t run out of time trying to spawn new threads each time I found trie leaves, but I ran out of space, no matter how I did it. So, keeping track of all the leaves at a certain node of the trie AND summing them all up for each bit before spawning a new thread were forms of memoization - I kept track of how many words ended on that bit, rather than checking each one.
I used C! I had two structs, one for the nodes of the trie and one for the search threads.
I used linked lists for both, to make it easy to insert and delete. There was no disadvantage to using a linked list for the search threads because I had to step through each one anyway for each bit in the message.
That was fun!

"""

test = 5

# code pour tester le script hors site


if test == 1:  # 1 lettre

    inputs = [
        "..-",
        "6",
        "A",
        "B",
        "C",
        "HELLO",
        "K",
        "U",
        "WORLD",
    ]

    output = 1


"""
# test forum

# inputs = [".", "2", "E", "EEE"]

# output = 1

# test forum

# inputs = ["....----", "4", "E", "EE", "T", "TT"]
# output = 25

# test forum

# inputs = ["...----", "4", "E", "EE", "T", "TT"]
# output = 15
"""

if test == 2:  # Détection correcte d'un mot
    inputs = ["--.-------..", "5", "GOD", "GOOD", "MORNING", "G", "HELLO"]
    output = 1


if test == 3:  # simples messages
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


# test 4

# test 5
if test == 5:
    inputs = ["-.-..---.-..---.-..--", "5", "CAT", "KIM", "TEXT", "TREM", "CEM"]
    output = 125


# test 6 : LC,LD

if test == 6:

    inputs = ["..............................................", "2", "E", "I"]
    output = 2971215073
"""
inputs = [
    "-....--.-.-....--.-.",
    "3",
    "BAC",
    "BANN",
    "DUTETE",
]

output = 9
"""
# test 6 custom
if test == 6.1:
    inputs = [".............................", "2", "E", "I"]
    output = 832040

generator = (input for input in inputs)  # type: ignore


def input():
    return next(generator)


########################################################################################################################################


import sys  # noqa: E402
from collections import defaultdict, Counter  # noqa: E402
import time  # noqa: E402
from functools import lru_cache  # noqa: E402

start_time = time.perf_counter()

DEBUG_MODE = 1


def eprint(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, file=sys.stderr, flush=True, **kwargs)


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
# word_max_length = max([len(word) for word in words])

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
        eprint(sequence, "ends at", index)
        return 1

    # parent returns sum of children score
    for morse in unique_morses:
        if sequence.startswith(morse, index):
            eprint(sequence, "starts with", morse)
            score += DP_recursive_decode(index + len(morse))

    return score


result = DP_recursive_decode(0)

print(result)
eprint(result == output)  # type: ignore
