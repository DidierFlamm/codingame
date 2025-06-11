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

# code pour tester le script hors site

# test 1 : 1 letter

entries = [
    "-.-",
    "6",
    "A",
    "B",
    "C",
    "HELLO",
    "K",
    "WORLD",
]

output = 1

# test forum

# entries = [".", "2", "E", "EEE"]

# output = 1

# test forum

# entries = ["....----", "4", "E", "EE", "T", "TT"]
# output = 25

# test forum

# entries = ["...----", "4", "E", "EE", "T", "TT"]
# output = 15

entries = ["--.-------..", "5", "GOD", "GOOD", "MORNING", "G", "HELLO"]

output = 1

"""
# test 3 : simples messages

entries = [
    "......-...-..---.-----.-..-..-..",
    "5",
    "HELL",
    "HELLO",
    "OWORLD",
    "WORLD",
    "TEST",
]

output = 2
"""

# => 2

# test 4

# test 5
# entries = ["-.-..---.-..---.-..--", "5", "CAT", "KIM", "TEXT", "TREM", "CEM"]

# => 125

# test 6 : LC,LD

# entries = ["..............................................", "2", "E", "I"]
# output = 2971215073
"""
entries = [
    "-....--.-.-....--.-.",
    "3",
    "BAC",
    "BANN",
    "DUTETE",
]

output = 9
"""
# test 6 custom

# entries = [".............................", "2", "E", "I"]
# output = 832040

generator = (entry for entry in entries)


def input():
    return next(generator)


########################################################################################################################################


import sys  # noqa: E402
from collections import defaultdict, Counter  # noqa: E402
import time  # noqa: E402

start_time = time.perf_counter()


MODE = "str"

LOG_MODE = 1


def log(*args, **kwargs):
    if LOG_MODE:
        print(*args, **kwargs, file=sys.stderr, flush=True)


########################################################################################################################################

from collections import defaultdict, Counter  # noqa: E402, F811


MODE = "str"


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

if MODE == "str":

    inv_morse = {value: key for key, value in list(morse.items())}

    l_ = input()
    n = int(input())
    words = [input() for _ in range(n)]
    word_max_length = max([len(word) for word in words])

    # compute tous les morse des mots du dictionnaire
    codes = []

    def encode(word):
        code = ""
        for l_ in word:
            code += inv_morse[l_]
        return code

    for word in words:
        codes.append(encode(word))

    # compute code_counter

    code_counter = Counter(codes)
    unique_codes = [key for key in list(code_counter.keys())]
    get_code_variants = [value for value in list(code_counter.values())]

    # et leur longueur
    get_code_length = [len(code) for code in unique_codes]

    code_max_length = max([len(code) for code in unique_codes])

    morse_dict = {"": l_}
    memo = defaultdict(list)
    mismatch = []
    go_on = True

    def compute_dict(morse_dict, memo, code_max_length):
        go_on = False
        # récupère les chemins terminés
        new_dict = {key: value for key, value in list(morse_dict.items()) if not value}
        # traite les chemins non terminés
        for key, value in list(morse_dict.items()):

            # branche terminée on passe à la clé suivante
            if not value:
                continue

            # branche non terminée
            head = value[:code_max_length]

            # si head déjà connue, on consulte memo
            if head in memo:
                for idx in memo[head]:
                    # log("get memo", idx)
                    remaining = value[get_code_length[idx] :]
                    new_dict[key + f"_{idx}"] = remaining
                    if len(remaining):
                        go_on = True

            # si head pas connue, on ajoute dans memo
            else:
                for idx, code in enumerate(unique_codes):
                    if head.startswith(code):
                        #        found = True
                        remaining = value[len(code) :]
                        new_dict[key + f"_{idx}"] = remaining
                        if len(remaining):
                            go_on = True
                        # log("memo", idx)
                        memo[head].append(idx)

        return new_dict, memo, go_on

    while go_on:
        morse_dict, memo, go_on = compute_dict(morse_dict, memo, code_max_length)
        # log(morse_dict)

    # compute result
    result = 0
    for path in list(morse_dict.keys()):
        result_path = 1
        for idx in path[1:].split("_"):
            # log(get_code_variants[int(idx)])
            result_path *= get_code_variants[int(idx)]
        result += result_path


if MODE == "int":

    inv_morse = {value: key for key, value in list(morse.items())}

    l_ = input()
    n = int(input())
    words = [input() for _ in range(n)]

    # compute tous les morse des mots du dictionnaire
    codes = []

    def encode(word):
        code = ""
        for l_ in word:
            code += inv_morse[l_]
        return code

    for word in words:
        codes.append(encode(word))

    # compute code_counter

    code_counter = Counter(codes)
    unique_codes = [key for key in list(code_counter.keys())]
    nb_unique_codes = len(unique_codes)
    get_code_count = [value for value in list(code_counter.values())]

    # et leur longueur
    get_code_length = [len(code) for code in unique_codes]
    code_max_length = max(get_code_length)  # sert à déterminer la taille du head

    nb_unique_codes_length = len(str(nb_unique_codes))

    separator = nb_unique_codes  # nb correspond à l'indice max +1

    pad = 10 * len(str(separator))

    log("l_=", l_)
    log("words =", words)
    log("codes =", codes)
    log("unique_codes =", unique_codes)
    log("code_counter =", code_counter)
    log("code_max_length =", code_max_length)
    log("separator=", separator)
    log("pad =", pad)

    morse_dict_str = {
        "": l_
    }  # les codes des clés sont séparés par des _ : exemple : '_1_5_6_11_0'
    morse_dict_int = {
        0: l_
    }  # variante avec des clés int pour vérifier perf par rapport à str.
    # les codes sont séparés par des 0 : exemple : 10506011
    # problème je ne peux pas utiliser 0 comme indice de code => décalage de 1 : 0-> 1 , etc...
    memo = defaultdict(list)
    mismatch = []
    go_on = True

    def compute_dict_int(morse_dict, memo, code_max_length):
        global pad
        go_on = False
        # récupère les chemins terminés
        new_dict: dict[int, str] = {
            key: value for key, value in list(morse_dict.items()) if not value
        }
        # log("\nmorse_dict=", morse_dict)
        # traite les chemins non terminés
        for key, value in list(morse_dict.items()):
            # log("key=", key, "value=", value)
            # branche terminée on passe à la clé suivante
            if not value:
                continue

            # branche non terminée
            head = value[:code_max_length]
            # log("head=", head)
            # si head déjà connue, on consulte memo
            if head in memo:
                """log(
                    "head_inconnue=",
                    head,
                    "pad=",
                    pad,
                    "separator=",
                    separator,
                )"""
                for idx in memo[head]:
                    # log("get memo", idx)n
                    remaining = value[get_code_length[idx] :]

                    new_dict[(key * pad + separator) * pad + idx] = remaining
                    if len(remaining):
                        go_on = True

            # si head pas connue, on ajoute dans memo
            else:
                # log(
                #    "head_inconnue=",
                #    head,
                # )
                for idx, code in enumerate(unique_codes):
                    # log("code=", code, "head=", head)
                    if head.startswith(code):
                        remaining = value[len(code) :]
                        # log(f"new_key_{idx}=", (key * pad + separator) * pad + idx)
                        new_dict[(key * pad + separator) * pad + idx] = remaining
                        if len(remaining):
                            go_on = True
                        # log("memo", idx)
                        memo[head].append(idx)

        return new_dict, memo, go_on

    while go_on:
        morse_dict, memo, go_on = compute_dict_int(
            morse_dict_int, memo, code_max_length
        )
        # log(morse_dict)

    # compute result
    result = 0
    for key in list(morse_dict_int.keys()):
        result_path = 1

        for idx in str(key).split(str(separator)):
            # log("key_final=", key)
            # log("idx_final=", idx)
            result_path *= get_code_count[int(idx)]
            # log(f"unique_code_{idx}=", unique_codes[int(idx)], "count=", result_path)
        result += result_path
        # log(result)


print(result)  # type: ignore
