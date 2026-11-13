import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, RadioButtons

#wczytywanie plikow
def wczytaj_wzorzec_z_pliku(sciezka_do_pliku):
    wiersze = []
    try:
        with open(sciezka_do_pliku, 'r', encoding='utf-8') as plik:
            for linia in plik:
                linia = linia.strip()
                if not linia:
                    continue
                nowy_wiersz = [1 if znak == 'O' else 0 for znak in linia]
                wiersze.append(nowy_wiersz)
    except Exception as blad:
        print(f"Nie udało się odczytać pliku {sciezka_do_pliku}: {blad}")
        return np.array([[1]], dtype=int)

    if not wiersze:
        return np.array([[1]], dtype=int)

    najwieksza_szerokosc = max(len(w) for w in wiersze)
    for wiersz in wiersze:
        brakuje = najwieksza_szerokosc - len(wiersz)
        wiersz.extend([0] * brakuje)

    return np.array(wiersze, dtype=int)


def szukaj_plikow_txt():
    pliki = [element for element in os.listdir('.') if element.endswith('.txt')]
    return pliki


#symulacja
class SymulacjaGraWZycie:
    def __init__(self, rozmiar=200, max_krokow=50):
        self.rozmiar = rozmiar
        self.max_krokow = max_krokow        
        self.plansza = np.zeros((rozmiar, rozmiar), dtype=int)
        self.brzeg = 'periodyczny'        # 'periodyczny' lub 'odbijajacy'
        self.regula = 'Conway (B3/S23)'   # Conway lub Wlasna (B35/S234)
        self.licznik_krokow = 0
        self.czy_dziala = True

    def umieszcz_wzorzec(self, nazwa_pliku):
        self.plansza.fill(0)
        self.licznik_krokow = 0
        self.czy_dziala = True            

        wzorzec = wczytaj_wzorzec_z_pliku(nazwa_pliku)
        wysokosc, szerokosc = wzorzec.shape

        wysokosc = min(wysokosc, self.rozmiar)
        szerokosc = min(szerokosc, self.rozmiar)
        wzorzec = wzorzec[:wysokosc, :szerokosc]

        srodek_wiersz = (self.rozmiar - wysokosc) // 2
        srodek_kolumna = (self.rozmiar - szerokosc) // 2

        self.plansza[srodek_wiersz : srodek_wiersz + wysokosc, 
                     srodek_kolumna : srodek_kolumna + szerokosc] = wzorzec

    def zrob_krok(self):
        if self.licznik_krokow >= self.max_krokow:
            self.czy_dziala = False
            return

        N = self.rozmiar
        idx = np.arange(N)

        # 1. Wybór trybu brzegów (modulo vs odbicie)
        if self.brzeg == 'periodyczny':
            gora  = (idx - 1) % N
            dol   = (idx + 1) % N
            lewo  = (idx - 1) % N
            prawo = (idx + 1) % N
        else: 
            gora  = np.clip(idx - 1, 0, N - 1)
            dol   = np.clip(idx + 1, 0, N - 1)
            lewo  = np.clip(idx - 1, 0, N - 1)
            prawo = np.clip(idx + 1, 0, N - 1)

            # Odbicie krawędzi zewnętrznych
            gora[0] = 1
            dol[-1] = N - 2
            lewo[0] = 1
            prawo[-1] = N - 2

        # 2. Zliczanie 8 sąsiadów
        sasiadzi = (
            self.plansza[gora][:, lewo]  + self.plansza[gora]  + self.plansza[gora][:, prawo] +
            self.plansza[:, lewo]                             + self.plansza[:, prawo] +
            self.plansza[dol][:, lewo]   + self.plansza[dol]   + self.plansza[dol][:, prawo]
        )

        # 3. Reguły przejścia
        if self.regula == 'Conway (B3/S23)':
            narodziny = (sasiadzi == 3)
            przetrwanie = (self.plansza == 1) & ((sasiadzi == 2) | (sasiadzi == 3))
        else:  #  B35/S234
            narodziny = (sasiadzi == 3) | (sasiadzi == 5)
            przetrwanie = (self.plansza == 1) & ((sasiadzi >= 2) & (sasiadzi <= 4))

        self.plansza = (narodziny | przetrwanie).astype(int)
        self.licznik_krokow += 1

        if self.licznik_krokow >= self.max_krokow:
            self.czy_dziala = False


#GUI
def uruchom_aplikacje():
    pliki_txt = szukaj_plikow_txt()

    sim = SymulacjaGraWZycie(rozmiar=200, max_krokow=50)
    sim.umieszcz_wzorzec(pliki_txt[0])

    fig, ax = plt.subplots(figsize=(11, 8))
    plt.subplots_adjust(left=0.28, bottom=0.15)

    obraz = ax.imshow(sim.plansza, cmap='binary', interpolation='nearest')
    ax.axis('off')

    def odswiez_tytul():
        status = "STOP" if not sim.czy_dziala else "START"
        if sim.licznik_krokow >= sim.max_krokow:
            status = "LIMIT 50 KROKÓW"
        ax.set_title(f"Krok: {sim.licznik_krokow}/{sim.max_krokow} [{status}]  |  Reguła: {sim.regula}  |  Brzeg: {sim.brzeg}", fontsize=11)

    odswiez_tytul()

    # przyciski
    ax_pat = plt.axes([0.02, 0.55, 0.22, 0.35])
    radio_pat = RadioButtons(ax_pat, pliki_txt)

    ax_bound = plt.axes([0.02, 0.35, 0.22, 0.15])
    radio_bound = RadioButtons(ax_bound, ('periodyczny', 'odbijajacy'))

    ax_rule = plt.axes([0.02, 0.15, 0.22, 0.15])
    radio_rule = RadioButtons(ax_rule, ('Conway (B3/S23)', 'Wlasna (B35/S234)'))

    ax_btn_run = plt.axes([0.35, 0.03, 0.18, 0.06])
    btn_run = Button(ax_btn_run, 'Start / Pauza')

    ax_btn_reset = plt.axes([0.60, 0.03, 0.18, 0.06])
    btn_reset = Button(ax_btn_reset, 'Reset')

    # OBSŁUGA ZDARZEŃ 
    def obsluga_zmiany_wzorca(nazwa_pliku):
        sim.umieszcz_wzorzec(nazwa_pliku)
        obraz.set_data(sim.plansza)
        odswiez_tytul()
        fig.canvas.draw_idle()

    def obsluga_zmiany_brzegow(etykieta):
        sim.brzeg = etykieta
        odswiez_tytul()

    def obsluga_zmiany_reguly(etykieta):
        sim.regula = etykieta
        odswiez_tytul()

    def obsluga_pauzy(event):
        if sim.licznik_krokow < sim.max_krokow:
            sim.czy_dziala = not sim.czy_dziala
            odswiez_tytul()
            fig.canvas.draw_idle()

    def obsluga_resetu(event):
        sim.umieszcz_wzorzec(radio_pat.value_selected)
        obraz.set_data(sim.plansza)
        odswiez_tytul()
        fig.canvas.draw_idle()

    radio_pat.on_clicked(obsluga_zmiany_wzorca)
    radio_bound.on_clicked(obsluga_zmiany_brzegow)
    radio_rule.on_clicked(obsluga_zmiany_reguly)
    btn_run.on_clicked(obsluga_pauzy)
    btn_reset.on_clicked(obsluga_resetu)

    def aktualizuj_klatke(frame):
        if sim.czy_dziala:
            sim.zrob_krok()
            obraz.set_data(sim.plansza)
            odswiez_tytul()
        return [obraz]

    anim = FuncAnimation(fig, aktualizuj_klatke, interval=40, blit=False)
    plt.show()


if __name__ == "__main__":
    uruchom_aplikacje()