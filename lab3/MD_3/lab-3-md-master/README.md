# LAB - 3 - Automaty komórkowe 1D

## Cel zadania
Zamiast standardowego automatu binarnego, wykorzystaj koncepcję automatu komórkowego 1D do zamodelowania prostego zjawiska (do wyboru: **korek uliczny na jednopasmowym rondzie**, **rozprzestrzenianie się pożaru w lesie** lub **własny pomysł**).

## Punktacja (max 20 pkt)

1. **Przestrzeń i warunek brzegowy (10 pkt)**
   - Inicjalizacja przestrzeni 1D o rozmiarze i liczbie kroków podawanych przez użytkownika (z obsługą błędów wejścia).
   - Zastosowanie periodycznego warunku brzegowego (zamknięta pętla) ORAZ porównawczo warunku pochłaniającego/odbijającego (ściana na końcach tablicy).
   - Możliwość wprowadzania własnych reguł 

2. **Złożone sąsiedztwo lub stany (10 pkt)**
   - Komórka musi posiadać minimum 3 stany (np. dla pożaru: `0 - puste pole`, `1 - drzewo`, `2 - płonące drzewo`) LUB uwzględniać sąsiedztwo o promieniu r=2 (po dwóch sąsiadów z każdej strony).
   - Opracuj własny zestaw reguł opisujący wybrane zjawisko (np. „drzewo płonie, jeśli minimum jeden sąsiad płonie, ale w kolejnym kroku zamienia się w puste pole”).
   - Zapisz regułę w formie zakodowanej (liczba / ciąg znaków), tak aby program potrafił ją odczytać z wejścia i zbudować z niej logikę przejść.
   - Zbadaj, przy jakim początkowym zagęszczeniu (np. procent aut na drodze lub drzew w lesie) układ się blokuje / całkowicie wypala. Przygotuj 2-3 predefiniowane scenariusze testowe do uruchomienia na zajęciach.

## Bonus (+5 pkt)
- Czynnik losowy (automat probabilistyczny – np. 10% szans na samozapłon lub nagłe hamowanie) wraz ze statystyką podsumowującą na końcu symulacji (np. wykres tekstowy liczby żywych komórek w kolejnych iteracjach).
