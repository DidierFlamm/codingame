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

# code pour tester le script hors site
entries = [
    "......-...-..---.-----.-..-..-..",
    "5",
    "HELL",
    "HELLO",
    "OWORLD",
    "WORLD",
    "TEST",
]




# test 5
entries = ["-.-..---.-..---.-..--", "5", "CAT", "KIM", "TEXT", "TREM", "CEM"]

# => 125

# test 6

#entries = ["..............................................", "2", "E", "I"]

# => 2971215073


generator = (entry for entry in entries)


def input():
    return next(generator)


######################################


import sys  # noqa: E402
from collections import defaultdict  # noqa: E402
import time

start_time = time.perf_counter()

def log(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr, flush=True)


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

l_ = input()
n = int(input())
words = [input() for _ in range(n)]
word_max_length = max([len(word) for word in words])

log("l_=", l_)
log("words =", words)

log("word_max_length =", word_max_length)

# compute tous les morse des mots du dictionnaire
codes = []

def encode(word):
    code = ""
    for l_ in word:
        code += inv_morse[l_]
    return code


for word in words:
    codes.append(encode(word))

# et leur longueur
get_code_length = [len(code) for code in codes]

code_max_length = max([len(code) for code in codes])

log("code_max_length =", code_max_length)
log("codes =", codes)

morse_dict = {"": l_}
memo = defaultdict(list)
mismatch = []
go_on = True



def compute_dict(morse_dict, match, mismatch, code_max_length):
    go_on = False
    new_dict = {key: value for key, value in list(morse_dict.items()) if not value}
    for key, value in list(morse_dict.items()):
        head = value[:code_max_length]
        
        #si déjà connu
        if head in memo:
            for idx in memo[head]:
                remaining = value[get_code_length[idx] :]
                new_dict[key + f"_{idx}"] = remaining
                if len(remaining):
                    go_on = True

        
        else:
            for idx, code in enumerate(codes):
                if head.startswith(code):
            #        found = True
                    remaining = value[len(code) :]
                    new_dict[key + f"_{idx}"] = remaining
                    if len(remaining):
                        go_on = True
                    memo[head].append(idx)
                    #log(memo)
        
        #if not found:
        #    mismatch.append(head)
    return new_dict, memo, mismatch, go_on


while go_on:
    morse_dict, match, mismatch, go_on = compute_dict(
        morse_dict, memo, mismatch, code_max_length
    )
    log(memo)

# dict_alpha_morse = finalize_dict(dict_alpha_morse)

result = len(morse_dict)

print(result)

print(time.perf_counter()-start_time)
