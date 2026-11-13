import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def epidemic_logic(kod_str):
    if len(kod_str) != 27:
        raise ValueError("Kod musi zawierac 27 cyfr!")

    tab = {}
    idx =0 # stan 0, 1 lub 2
    for left in (0,1,2):
        for middle in (0,1,2):
            for right in (0,1,2):
                tab[(left,middle,right)]=int(kod_str[idx]) #zmiana ciągu znakow na regule
                idx += 1
    return tab

def in_population(size, resistance):
    population = np.zeros(size, dtype=int)

    resis_mask = np.random.rand(size) < resistance  # losowanie odpornych
    population[resis_mask] = 2 #zaznaczenie kolorem szarym odpornych
    population[size //2] =1 #pacjent 0
    
    return population

def sym_epidemic(size, steps, resistance, kod_str):
    tab = epidemic_logic(kod_str)
    archi = np.zeros((steps, size), dtype=int)
    archi[0] = in_population(size, resistance)

    for s in range(1, steps):
        prev = archi[s-1]
        for i in range(size):
            left = int(prev[(i-1) % size])
            middle = int(prev[i])
            right = int(prev[(i+1) % size])

            archi[s,i] = tab[(left, middle, right)]
    return archi


# --- parametry symulacji---
kod = "112112021211202102010022012"
size = 100
steps = 60
resistance = 0.2 # ...% osób w populacji ma już odporność

historia = sym_epidemic(size, steps, resistance, kod)

# Mapowanie kolorów
cmap = ListedColormap(['green', 'red', 'gray'])

plt.figure(figsize=(10, 6))
plt.imshow(historia, cmap=cmap, vmin=0, vmax=2, interpolation='nearest')
plt.title(f"Model Epidemii (Odporność populacyjna = {int(resistance*100)}%)")
plt.xlabel("Rozmiar")
plt.ylabel("Czas (kroki)")
plt.show()
