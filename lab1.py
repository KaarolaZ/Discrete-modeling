import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 

nazwa_pliku = "Pan_zywiec_zdroj_wynalazca_wody.png"
obraz_org = Image.open(nazwa_pliku).convert("RGB")
obraz_na_liczby = np.array(obraz_org)

#Średnia 
szary_1 = np.mean(obraz_na_liczby, axis=2).astype(np.uint8)

#Ucięcie kanałów
szary_2 = obraz_na_liczby[:,:,0]

fig, axs = plt.subplots(1,2, figsize=(10,5))
axs[0].imshow(szary_1, cmap='gray')
axs[0].set_title('Zastosowanie średniej')
axs[1].imshow(szary_2, cmap='gray')
axs[1].set_title('Pozostawienie jednego kanału')
plt.show()

#Ściemnienie
procent = 44
jasnosc = 1.0-(procent/100)

obraz_sciemniony=np.clip(obraz_na_liczby*jasnosc, 0, 255).astype(np.uint8)
plt.imshow(obraz_sciemniony)
plt.title(f'Zaciemnienie obrazu o {procent} procent')
plt.show()

#rozjaśnianie
obrazy=[]
for liczba in range(10, 21):
    rozjasnienie= 1.0 +(liczba/100)
    obraz_rozjaśniony=np.clip(obraz_na_liczby*rozjasnienie, 0, 255).astype(np.uint8)
    obrazy.append(obraz_rozjaśniony)

ilosc=len(obrazy)
fig, axs = plt.subplots(1, ilosc, figsize=(20,4))
for i in range(ilosc):
    axs[i].imshow(obrazy[i], cmap='gray')
    axs[i].set_title(f"{10+i}%")
    axs[i].axis('off')
    
plt.show()


#binaryzacja 1
prog =127
obraz_binarny = np.where(szary_1>prog, 255, 0).astype(np.uint8)
plt.imshow(obraz_binarny, cmap='gray')
plt.title('Binaryzacja z progiem 50%')
plt.show()

# binaryzacja 2
prog_user= int(input('Podaj prog binaryzacji % (np. 30): '))
nowy_prog = (prog_user/100)*255
obraz_binarny2 = np.where(szary_1>nowy_prog, 255, 0).astype(np.uint8)
plt.imshow(obraz_binarny2, cmap='gray')
plt.title(f'Binaryzacja z progiem {prog_user}%')
plt.show()
