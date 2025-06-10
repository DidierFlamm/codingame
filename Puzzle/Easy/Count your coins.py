"""
https://www.codingame.com/training/easy/count-your-coins

Objectif
You live in a world where all coins have the same shape, weight and feel. You can't distinguish them in your pocket. Knowing how many coins of each value you have in your pocket, how many should you grab, without looking, to be sure to have enough money to pay?

Entrée
Line 1 : An integer valueToReach representing the price you want to be able to pay
Line 2 : An integer N representing the number of different coin types you have
Line 3 : N integers separated by space representing the number of coins of each type
Line 4 : N integers separated by space representing the value of each type

Sortie
Line 1 : A line containing a single integer representing the minimum number of coins you need to grab to be sure to have enough money to pay. -1 if there's not enough money in your pocket

Contraintes
1<= number of coins <=1000
1<= coin values <=1000
1<= N <=1000

Exemple
Entrée
8
1
5
6
Sortie
2

"""

# code pour tester le script hors site
entries = ["8", "1", "5", "6"]

generator = (entry for entry in entries)


def input():
    return next(generator)


######################################

value_to_reach = int(input())
n = int(input())
counts = [int(i) for i in input().split()]
values = [int(i) for i in input().split()]
coins = dict(sorted({value: count for value, count in zip(values, counts)}.items()))

money = 0
n_coins = 0
enough = False

for item in list(coins.items()):
    for _ in range(item[1]):
        n_coins += 1
        money += item[0]
        if money >= value_to_reach:
            print(n_coins)
            enough = True
            break
    if enough:
        break

if not enough:
    print("-1")
