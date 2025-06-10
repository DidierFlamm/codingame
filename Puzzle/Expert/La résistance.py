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

inv_morse = {value: key for key, value in list(morse.items())}

import sys  # noqa: E402


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


l_ = input()
n = int(input())
words = [input() for _ in range(n)]
word_max_length = max([len(word) for word in words])

log(l_)
log(words)

log("word max length:", word_max_length)

# memoize tous les morse des mots du dictionnaire
memo_words = []


def encode(word):
    code = ""
    for l_ in word:
        code += inv_morse[l_]
    return code


for word in words:
    memo_words.append(encode(word))

log(memo_words)


def decode_head(string):
    dict_head = {}
    string_head = string[:word_max_length]
    string_tail = string[word_max_length:]

    for length in range(1, 5):  # max 4 signes par lettre en morse
        for code in list(morse.keys()):
            if code == string[:length] and len(code) == length:
                dict_head[morse[code]] = string[length:]

    # memo_head[string_head]=

    return dict_head


# 1ere lettre
def init_dict(string):
    dict_init = decode_head(string)
    log(dict_init)

    # purge des clés qui ne sont pas compatibles avec words

    dict_temp = dict_init

    dict_init = {}

    for key, value in dict_temp.items():
        for word in words:
            if word.startswith(key):
                dict_init[key] = value
                # if key == word:
                #    dict_init[key + "_"] = value
                break

    log(dict_init)

    return dict_init


# lettre suivante
def next_dict(dict_alpha_morse):
    global mismatch

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
