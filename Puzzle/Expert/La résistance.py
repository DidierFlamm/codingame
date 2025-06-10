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

# entries = ["..............................................", "2", "E", "I"]

# => 2971215073


generator = (entry for entry in entries)


def input():
    return next(generator)


######################################


morse = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
}


import sys  # noqa: E402
from collections import defaultdict  # noqa: E402


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

# memoize tous les morse des mots du dictionnaire
codes = []


def encode(word):
    code = ""
    for l_ in word:
        code += inv_morse[l_]
    return code


for word in words:
    codes.append(encode(word))

code_max_length = max([len(code) for code in codes])

log("code_max_length =", code_max_length)
log("codes =", codes)

morse_dict = {"": l_}
match = defaultdict(list)
mismatch = []


def compute_dict(morse_dict, match, mismatch, code_max_length):
    new_dict = {key: value for key, value in list(morse_dict.items()) if not value}
    for key, value in list(morse_dict.items()):
        head = value[:code_max_length]
        found = False
        for code in codes:
            if head.startswith(code):
                found = True
                remaining = value[len(code) :]
                new_dict[key + "_" + code] = remaining
                if len(remaining):
                    go_on = True
                match[head].append(morse)
        if not found:
            mismatch.append(head)
    return new_dict, match, mismatch


for _ in range(100):
    morse_dict, match, mismatch = compute_dict(
        morse_dict, match, mismatch, code_max_length
    )
    log(morse_dict)

# dict_alpha_morse = finalize_dict(dict_alpha_morse)

result = len(morse_dict)

print(result)

"""
# mot suivant
def next_dict(morse_dict, match, mismatch):
    next_morse_dict
    
        temp_dict = 
        next_morse_dict[]


    # ajoute les différentes possibilité de 'prochaine lettre' à toutes les clés si c'est pas un mismatch connu

    for cle, value in list(dict_alpha_morse.items()):
        if value:
            del dict_alpha_morse[cle]
            dict_temp = decode_head(value)

            for key_temp, value_temp in list(dict_temp.items()):
                if cle.split("_")[-1] + key_temp not in memo_mismatch:
                    dict_alpha_morse[cle + key_temp] = value_temp

    log(dict_alpha_morse)

    # purge des clés qui ne sont pas compatibles avec words

    dict_temp = dict_alpha_morse

    dict_alpha_morse = {}

    for key, value in dict_temp.items():

        for word in words:

            last_key = key.split("_")[-1]

            # si la fin de clé correspond à un mot, et qu'il reste du morse, on ajoute la clé avec _
            if last_key == word and value:
                dict_alpha_morse[key + "_"] = value

            # si la fin de clé correspond au début d'un mot, on ajoute la clé
            elif word.startswith(last_key):
                dict_alpha_morse[key] = value
                break

            # sinon ajoute la fin de clé aux mismatch
            else:
                memo_mismatch.add(last_key)

    # on pourrait sortir les clés terminées dans une liste à part pour réduire la taille du dictionnaire

    log(dict_alpha_morse)

    return dict_alpha_morse


memo_mismatch = set()

dict_alpha_morse = init_dict(l_)

for _ in range(10):
    dict_alpha_morse = next_dict(dict_alpha_morse)

# dict_alpha_morse = finalize_dict(dict_alpha_morse)

result = len(dict_alpha_morse)

print(len(dict_alpha_morse))
"""
