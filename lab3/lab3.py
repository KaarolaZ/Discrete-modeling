import numpy as np
import matplotlib.pyplot as plt

def pobierz_dane():
    while True:
        try:
            rozmiar = int(input("Podaj rozmiar: "))
            krok = int(input("Podaj krok: "))

            if rozmiar >0 and krok>0 : 
                return rozmiar, krok
            else:
                print("Podaj nieujemne wartosci")

        except ValueError:
            print("Blad, wprowadz liczbe calkowita")

rozmiar, krok = pobierz_dane()
stan = np.zeros(rozmiar, dtype=int)
stan[rozmiar//2] = 1

#warunek periodyczny - lewym sąsiadem pierwszej komórki staje się ostatnia komórka z prawego końca
def periodic(stan, i, N):
    left = stan[(i-1)%N] 
    middle = stan[i] 
    right = stan[(i+1) %N] 
    return left, middle, right

#warunek pochlaniajacy
def absorbing(stan, i, N):
    left = stan[i-1] if i>0 else 0
    middle = stan[i] 
    right = stan[i+1] if i<N-1 else 0
    return left, middle, right

#warunek odbijajacy
def reflecting(stan, i, N):
    left = stan[i-1] if i>0 else stan[0]
    middle = stan[i]
    right = stan[i+1] if i<N-1 else stan[N-1]
    return left, middle, right

def create_rule(rule_number):
    binary = format(rule_number, '08b')
    return [int(bit) for bit in binary]

def use_rule(left, middle, right, bin_rule):
    id = left*4 + middle*2 + right*1
    return bin_rule[7-id]

rule_number = int(input("Podaj numer reguły (0 - 255): "))
new_rule = create_rule(rule_number)

archi = np.zeros((krok, rozmiar), dtype=int)
#stan poczatkowy
archi[0, rozmiar//2] =1

for s in range(1, krok):
    prev_step = archi[s-1]

    for i in range(rozmiar):
        left, middle, right = periodic(prev_step, i, rozmiar)
        #left, middle, right = absorbing(prev_step, i, rozmiar)
        # left, middle, right = reflecting(prev_step, i, rozmiar)

        archi[s, i]= use_rule(left, middle, right, new_rule)

plt.figure(figsize=(10, 6))
plt.imshow(archi, cmap='binary', interpolation='nearest')
plt.title(f"Automat 1D - Regula {rule_number}")
plt.xlabel("Przestrzeń (komórki)")
plt.ylabel("Czas (kroki)")
plt.show()