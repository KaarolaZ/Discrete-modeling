import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

image_path="Pan_zywiec_zdroj_wynalazca_wody.png"
image = Image.open(image_path).convert('L') 
image_szary = np.array(image, dtype=np.float32)

image_bin = np.where(image_szary > 127, 255, 0).astype(np.uint8)

def dylatacja(obraz, promien):
    wys, szer = obraz.shape
    wynik =np.zeros_like(obraz)

    obraz_pad = np.pad(obraz, promien, mode='constant', constant_values=0) 
    for y in range(wys):
        for x in range(szer):
            okienko = obraz_pad[y : y + 2*promien + 1, x : x + 2*promien + 1]    
            wynik[y, x] = np.max(okienko)            
    return wynik

def erozja(obraz, promien):
    wys, szer = obraz.shape
    wynik =np.zeros_like(obraz)
     
    obraz_pad = np.pad(obraz, promien, mode='constant', constant_values=255) 
    for y in range(wys):
        for x in range(szer):
            okienko = obraz_pad[y : y + 2*promien + 1, x : x + 2*promien + 1]
            wynik[y, x] = np.min(okienko)
    return wynik




def otwarcie(obraz, promien):
    return dylatacja(erozja(obraz, promien), promien)

def zamkniecie(obraz, promien):
    return erozja(dylatacja(obraz, promien), promien)



i= int(input("Podaj promien (min 3, max 10): "))
if (i < 3 or i>10 ):
    print("Podales zla wartosc")
    i= int(input("Podaj promien (min 3, max 10): "))

obraz_dylatacja = dylatacja(image_bin, promien= i)
obraz_erozja = erozja(image_bin, promien= i)
obraz_otwarcie = otwarcie(image_bin,promien=  i)
obraz_zamkniecie = zamkniecie(image_bin,promien= i)

fig, axs = plt.subplots(1,5, figsize=(25,5))
axs[0].imshow(image_szary, cmap='gray')
axs[0].set_title('obraz oryginalny')
axs[1].imshow(obraz_dylatacja, cmap='gray')
axs[1].set_title('Dylatacja')
axs[2].imshow(obraz_erozja,cmap='gray' )
axs[2].set_title('Erozja')
axs[3].imshow(obraz_otwarcie,cmap='gray' )
axs[3].set_title('Otwarcie')
axs[4].imshow(obraz_zamkniecie,cmap='gray' )
axs[4].set_title('Zamkniecie')
plt.show()


def splot(obraz, kernel):
    kernel_flipped = np.flipud(np.fliplr(kernel))
    wysokosc, szerokosc = obraz.shape
    # Zakładamy kwadratowy kernel o nieparzystym rozmiarze
    promien = kernel.shape[0] // 2 
    wynik = np.zeros_like(obraz, dtype=np.float32)
     
    obraz_pad = np.pad(obraz, promien, mode='edge')
    
    for y in range(wysokosc):
        for x in range(szerokosc):
            okienko = obraz_pad[y : y + 2*promien + 1, x : x + 2*promien + 1]
            # Mnożymy wartości okienka przez maskę i sumujemy
            wynik[y, x] = np.sum(okienko * kernel_flipped)

    
    return np.clip(wynik, 0, 255).astype(np.uint8)

# r = int(input("Podaj promien dla splotu: "))
# rozmiar_maski = 2 * r + 1

# # Stworzenie maski uśredniającej 
# liczba_elementow = rozmiar_maski * rozmiar_maski
# moj_kernel = np.ones((rozmiar_maski, rozmiar_maski), dtype=np.float32) / liczba_elementow


# obraz_splot = splot(image_bin, moj_kernel)
# plt.imshow(obraz_splot, cmap='gray')
# plt.title('Splot')
# plt.show()


def gaussa(promien, sigma):
    # Tworzy dwuwymiarową maskę filtru Gaussa ze wzoru matematycznego.
    rozmiar = 2 * promien + 1
    kernel = np.zeros((rozmiar, rozmiar), np.float32)
    for y in range(rozmiar):
        for x in range(rozmiar):
            x_odleglosc = x - promien
            y_odleglosc = y - promien
            # Wzór na rozkład normalny
            kernel[y, x] = np.exp(-(x_odleglosc**2 + y_odleglosc**2) / (2 * sigma**2))
    # Suma wszystkich wag w masce musi wynosić 1, więc dzielimy przez sumę
    return kernel / np.sum(kernel)

#promien = 2 (maska 5x5), sigma = 1.0
gauss_podstawa = splot(image_szary, gaussa(promien=2, sigma=1.0))

# Modyfikacja 1: Większy rozmiar okna
gauss_duzy_promien = splot(image_szary, gaussa(promien=10, sigma=1.0))

# Modyfikacja 2: większa sigma
gauss_duza_sigma = splot(image_szary, gaussa(promien=2, sigma=10.0))

fig, axs = plt.subplots(1,3, figsize=(15,5))
axs[0].imshow(gauss_podstawa, cmap='gray')
axs[0].set_title('Gauss')
axs[1].imshow(gauss_duzy_promien, cmap='gray')
axs[1].set_title('gauss- wiekszy promien')
axs[2].imshow(gauss_duza_sigma,cmap='gray' )
axs[2].set_title('gauss- duza sigma')
plt.show()


#Gradient morfologiczny = Dylatacja odjąć Erozja 
# pokazuje kontury, krawędzie wszystkich jasnych kształtów widocznych na obrazie.
morf_gradient = np.clip(obraz_dylatacja.astype(np.int16) - obraz_erozja.astype(np.int16), 0, 255).astype(np.uint8)

#Top Hat = Oryginał odjąć Otwarcie (wydobywa jasne detale mniejsze niż promień na ciemnym tle)
morf_tophat = np.clip(image_bin.astype(np.int16) - obraz_otwarcie.astype(np.int16), 0, 255).astype(np.uint8)

#Black Hat = Domknięcie odjąć Oryginał (wydobywa ciemne detale mniejsze niż promień na jasnym tle)
morf_blackhat = np.clip(obraz_zamkniecie.astype(np.int16) - image_bin.astype(np.int16), 0, 255).astype(np.uint8)

fig, axs = plt.subplots(1,3, figsize=(15,5))
axs[0].imshow(morf_gradient, cmap='gray')
axs[0].set_title('Gradient morfologiczny')
axs[1].imshow(morf_tophat, cmap='gray')
axs[1].set_title('Top hat')
axs[2].imshow(morf_blackhat,cmap='gray' )
axs[2].set_title('Black hat')
plt.show()


# Filtr dolnoprzepustowy (uśredniający).Suma elementów wynosi 1.
kernel_dolno = np.loadtxt('dolno_przepustowy.txt', dtype=np.float32)
obraz_dolnoprzepustowy = splot(image_szary, kernel_dolno)

# Filtr górnoprzepustowy (wykrywanie krawędzi). Suma elementów wynosi 0.
kernel_gorno = np.loadtxt('gorno_przepustowy.txt', dtype=np.float32)
obraz_gornoprzepustowy = splot(image_szary, kernel_gorno)


fig, axs = plt.subplots(1,2, figsize=(10,5))
axs[0].imshow(obraz_dolnoprzepustowy, cmap='gray')
axs[0].set_title('Filtr dolnoprzepustowy')
axs[1].imshow(obraz_gornoprzepustowy, cmap='gray')
axs[1].set_title('Filtr gornoprzepustowy')
plt.show()