# Algorytm Alfa-Beta dla gry w Młynek

**[English version](README.md)**

## 1. ALGORYTM MINIMAX Z OBCINANIEM α – β

Algorytm minimax pozwala na określenie wartości funkcji oceny dla różnych stanów gry, prognozując *d* ruchy do przodu (głębokość). Algorytm działa rekurencyjnie do osiągnięcia głębokości *d* lub znalezienia węzła terminalnego (koniec gry). Co drugą iterację preferowana jest maksymalna wartość funkcji oceny spośród dostępnych ruchów, a naprzemiennie jej minimalna wartość (symulowanie optymalnych ruchów przeciwnika).

Wersja algorytmu minimax z obcinaniem α – β zapamiętuje ruch z najlepszą dotychczasową wartością (maksymalną / minimalną) i nie zagłębia się w ruch, który przeciwnik i tak nie wykonałby optymalnie (jeśli gra optymalnie), ponieważ są one dla niego niekorzystne. Taka metoda pozwala na znaczne przyspieszenie przeszukiwania. W Tabeli 1 przedstawiono czasy symulacji rozgrywki dla algorytmu minimax z i bez odcinania α – β (komentując linie odpowiedzialne za to – Fig.1):

![](img/fig_1.png)

*Fig. 1. Wyłącznie obcinanie alfa-beta.*

*Tabela 1. Czas działania algorytmu minimax bez i z obcinaniem alfa-beta.*

| GŁĘBOKOŚĆ (dla obu graczy) | Czas MINIMAX [s] | Czas MINIMAX α – β [s] |
| -------------------------- | ---------------- | ----------------------- |
| 1                          | 0.01             | 0.01                    |
| 2                          | 1.11             | 1.46                    |
| 3                          | 12.49            | 3.73                    |
| 4                          | 113.29           | 15.07                   |
| 5                          | 1117.26 (około 19 minut) | 37.09           |

Jak widać, wpływ obcinania alfa-beta na szybkość działania, szczególnie dla większych głębokości, jest ogromny. Algorytm alfa-beta pozwala na osiągnięcie równowagi pomiędzy dokładnością obliczeń a kosztem czasowym.

## 2. WPŁYW GŁĘBOKOŚCI PRZESZUKIWANIA

Przy niewystarczającej głębokości przeszukiwania algorytm może przeoczyć optymalne ruchy i doprowadzić do niekorzystnego wyniku. Z kolei zbyt duża głębokość przeszukiwania może prowadzić do zbyt długiego czasu obliczeń, znacznie spowalniając działanie algorytmu.

Oto przykład dużej różnicy głębokości pomiędzy graczami (5 i 1), jak widać statycznie, większa głębokość zwiększa szansę na wygraną:

![](img/fig_2.jpeg)

*Fig. 2. Statystyki rezultatów dla przykładowych głębokości przeszukiwań.*

*Tabela 2. Statystyki rezultatów algorytmu dla różnych kombinacji głębokości przeszukiwania.*

![](img/fig_3.png)

Analizując Tabelę 2, zauważamy minimalny wpływ algorytmu minimax na rezultaty rozgrywek – zazwyczaj wygrywa gracz z dużo większą głębokością przeszukiwań (lewy dolny i prawy górny róg). Jednakowoż, w ujęciu jednostkowym, nie są to wyniki zadowalające. Czynnikiem, który ma tu największy wpływ, jest funkcja heurystyczna, zwracająca wartość dla węzłów quasi-terminalnych (dojścia na wyznaczoną głębokość). Obecnie podaje ona jedynie różnicę pionków dwóch graczy. Aby ulepszyć funkcję oceny, można rozważyć dodanie dodatkowych punktów za "strategiczne" pozycje lub 2 pionki obok siebie (młynek możliwy w jednym ruchu). Takie rozwiązanie nie tylko wpłynie na skuteczność programu, ale może też przyśpieszyć jego działanie – większa rozpiętość możliwych funkcji oceny to większe szanse na obcięcie alfa-beta. Co więcej, maleje ryzyko, że wartość heurystyki będzie się powtarzała. Obecnie dzieje się to bardzo często, a zwracany jest losowy z tych ruchów.

## 3. WNIOSKI

Implementacja algorytmu minimax dla gry "Młynek" została zrealizowana pomyślnie. Jednakże skuteczność jego działania można zauważyć dopiero dla dużych różnic głębokości. W celu polepszenia rezultatów powinno się zdefiniować nową, bardziej zaawansowaną funkcję heurystyczną, której zakres zwracanych wartości jest znacznie większy niż 0, 1 lub 2 (jak w obecnym przypadku). Taką funkcję łatwiej byłoby stworzyć dla bardziej skomplikowanych gier, jak np. szachy, gdzie konkretne figury mają swoje wartości.

W sprawozdaniu pokazano ogromny wpływ obcinania alfa-beta, dzięki któremu dla 5 głębokości przeszukiwania udało się zmniejszyć czas z 19 minut na jedynie 30 sekund.

Podsumowując, implementacja algorytmu deterministycznego była w tym przypadku mocno poglądowa. Przy realnych zastosowaniach, funkcje oceny wartości i decyzje ruchów powinny być dużo bardziej zaawansowane. Algorytm symulował 100 rozgrywek, aby statystyki były bardziej dokładne. To dodatkowo wydłużyło czas oczekiwania na odpowiedź. Jednym z możliwych usprawnień kodu mogłoby być zastosowanie tzw. transpozycji tablicy, co pozwoliłoby na przyspieszenie obliczeń i uniknięcie wielokrotnego przeliczania tych samych stanów gry. Można to zrobić, przechowując wcześniej obliczone wartości heurystyki dla danego stanu gry w słowniku i korzystając z nich zamiast przeliczać je ponownie.
