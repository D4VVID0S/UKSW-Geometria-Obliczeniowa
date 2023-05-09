# Otoczka wypukła algorytmem Jarvisa (gift wrap)

Zainstaluj zalezności z pliku requirements.txt
`pip install -r requirements`

Uruchomienie programu
`python main.py -r`


### Opis programu

Program rysuje punkty (maksymalnie cztery), dla których następnie wyznacza otoczkę wypukłą zgodnie z algorytmem Jarvisa.
Kolejne kroki algorytmu mozna śledzic za pomocą animacji: podświetlenie poszczególnych punktów oraz odcinków. 
Odcinki podświetlone na zielono są typowane jako odcinki wchodzące w skład otoczki wypukłej. 
Ostatecznie otooczka wypukła jest narysowana za pomocą czerwonej linii.
W programie dostępny jest równiez log zdarzeń, który opisuje kroki algorytmu. Log jest równiez zapisywany do pliku, aby mozna było później sprawdzic prawidłowe działanie.
Po wykonaniu programu nalezy go zamknąc `ctrl + c`.

### Opis interfejsu programu

```
usage: main.py [-h] [-r | -n NUMBERS]

Program wizualizujący otoczkę wypukłą.

options:
  -h, --help            show this help message and exit
  -r, --random          Losowy zestaw czterech punktów
  -n NUMBERS, --numbers NUMBERS
                        Wpisz punkty, przykład: "(1,1),(2,2),(3,3)"
```

### Przykłady
- losowe punkty `python main.py -r`
- dla konkretnych punktów `python main.py -n "(10,34),(33,200),(100,25),(10,52)"`

### Ograniczenia
- punkty muszą znajdowac się w pierwszej cwiartce układu współrzędnych
- zakres wartości dla x to [0, 600], a y to [0, 700]
- maksymalna liczba punktów wynosi 4
- mimo, ze punkty będą w pierwszej cwiartce to ich prezentacja w programie jest lustrzanym odbiciem względem osi OX (wartośc y równa 0 znajduje się u góry, wartośc graniczna y znajduje się na dole ekranu)
