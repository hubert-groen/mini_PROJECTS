# Wielokryterialny model planowania produkcji z wykorzystaniem metody punktu odniesienia.

W celu sformułowania tego modelu posłużymy się funkcją satysfakcji:

f(x) = \sum_{i=1}^m \left( \begin{cases}
(x_i - a_i)^{2} / (a_i - r_i)^{2} & \text{dla } x_i \ge a_i \\
(x_i - r_i)^{2} / (a_i - r_i)^{2} & \text{dla } x_i < a_i
\end{cases} \right)

gdzie:

* `ai` to punkty aspiracji
* `ri` to punkty rezerwacji
* `β` to nachylenie funkcji po punkcie aspiracji
(symbolizuje dodatkowe zadowolenie użytkownika po przekroczeniu tego punktu)
* `γ` to nachylenie funkcji przed punktem rezerwacji
(symbolizuje niezadowolenie użytkownika z niespełnienia punktu rezerwacji)

Następnie całościową funkcję składającą się ze wszystkich kryteriów możemy zapisać w ten sposób:

f(x) = \max_{i=1}^m \left( \begin{cases}
(x_i - a_i)^{2} / (a_i - r_i)^{2} & \text{dla } x_i \ge a_i \\
(x_i - r_i)^{2} / (a_i - r_i)^{2} & \text{dla } x_i < a_i
\end{cases} \right)

oraz sformułować ograniczenia rozmyte:

\forall i \in \{1, \ldots, m\}:

x_i \ge a_i - \frac{r_i - a_i}{\beta_i}
x_i \le r_i + \frac{a_i - r_i}{\gamma_i}

Celowo zapisałem `β` oraz `γ` indeksem dolnym `i`, ponieważ w moim rozwiązaniu definiowałem nachylenie funkcji poza punktami aspiracji i rezerwacji osobno dla każdego kryterium, co daje użytkownikowi większą elastyczność w modelowaniu zdefiniowanego problemu.

W przedstawionym zadaniu mamy łącznie 5 ograniczeń rozmytych: `m = 5`.

# Parametry metody punkty odniesienia dla poszczególnych kryteriów:

| i | a | r | β | γ |
|---|---|---|---|---|
| 1 | 150 | 130 | 0.9 | 1.8 |
| 2 | 30 | 35 | 0.9 | 1.5 |
| 3 | 70 | 80 | 0.9 | 1.5 |
| 4 | 100 | 110 | 0.2 | 1 |
| 5 | 50 | 55 | 0.2 | 1 |

Jak widać w powyższym równaniu mamy maksymalizację podczas gdy niektóre z naszych funkcji chcemy minimalizować. Nie stanowi to jednak problemu, ponieważ i tak odpowiednio podstawiamy punkty aspiracji i rezerwacji, a wtedy `max` na powyższej sumie maksymalizuje naszą całkowitą funkcję satysfakcji.

# Ograniczenia ostra

x_1 + x_2 + x_3 + x_4 + x_5 = 100

x_1 \ge 0
x_2 \ge 0
x_3 \ge 0
x_4 \ge 0
x_5 \ge 0

Całościowy zapis powyższego modelu został przedstawiony w punkcie 4.
