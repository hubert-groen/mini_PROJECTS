set WYTWORNIE;
set MAGAZYNY;
set SKLEPY;
set PRODUKTY;

# PARAMETRY
param M;
param produkcja {PRODUKTY, WYTWORNIE} >= 0;
param zapotrzebowanie {PRODUKTY, SKLEPY} >= 0;
param koszty_W_to_M {WYTWORNIE, MAGAZYNY} >= 0;
param koszty_M_to_S {MAGAZYNY, SKLEPY} >= 0;


# ZMIENNE
var m1_1, binary;
var m2_1, binary;
var m2_2, binary;
var m3_n, integer;

var m1_quantity;
var m2_quantity;
var m3_quantity;

var m1_cost;
var m2_cost;
var m3_cost;

var ilosc_P1_W_to_M {WYTWORNIE, MAGAZYNY} >= 0;
var ilosc_P2_W_to_M {WYTWORNIE, MAGAZYNY} >= 0;
var ilosc_P1_M_to_S {MAGAZYNY, SKLEPY} >= 0;
var ilosc_P2_M_to_S {MAGAZYNY, SKLEPY} >= 0;



# FUNKCJA CELU

minimize F:     sum {w in WYTWORNIE, m in MAGAZYNY} ilosc_P1_W_to_M[w, m]*koszty_W_to_M[w, m]
            +   sum {w in WYTWORNIE, m in MAGAZYNY} ilosc_P2_W_to_M[w, m]*koszty_W_to_M[w, m]
            +   sum {m in MAGAZYNY, s in SKLEPY} ilosc_P1_M_to_S[m, s]*koszty_M_to_S[m, s]
            +   sum {m in MAGAZYNY, s in SKLEPY} ilosc_P2_M_to_S[m, s]*koszty_M_to_S[m, s]
            +   m1_cost + m2_cost + m3_cost;


# OGRANICZENIA

# ograniczenia pojemności i kosztów magazynu 1

s.t. og1:  m1_quantity >= 0;
s.t. og2:  m1_quantity <= 94 + M*m1_1;
s.t. og3:  m1_quantity >= 94 - M*(1-m1_1);
s.t. og4:  m1_quantity <= 109;
s.t. og5:  m1_quantity =    (sum {w in WYTWORNIE} ilosc_P1_W_to_M[w, 'M1'])
                          + (sum {w in WYTWORNIE} ilosc_P2_W_to_M[w, 'M1']);

s.t. og6:  m1_cost >= 348;
s.t. og7:  m1_cost >= 440 - M*(1-m1_1);

# ograniczenia pojemności i kosztów magazynu 2

s.t. og8:  m2_quantity >= 0;
s.t. og9:  m2_quantity <= 0 + M*m2_1;
s.t. og10: m2_quantity <= 88 + M*(1-m2_1);
s.t. og11: m2_quantity >= 88 - M*(1-m2_2);
s.t. og12: m2_quantity <= 109;
s.t. og13: m2_quantity =    (sum {w in WYTWORNIE} ilosc_P1_W_to_M[w, 'M2'])
                          + (sum {w in WYTWORNIE} ilosc_P2_W_to_M[w, 'M2']);

s.t. og14: m2_cost >= 0;
s.t. og15: m2_cost >= 324 - M*(1-m2_1);
s.t. og16: m2_cost >= 512 - M*(1-m2_2);

# ograniczenia pojemności i kosztów magazynu 3

s.t. og17: m3_quantity >= 0;
s.t. og18: m3_quantity <= 14*m3_n;
s.t. og19: m3_quantity =    (sum {w in WYTWORNIE} ilosc_P1_W_to_M[w, 'M3'])
                          + (sum {w in WYTWORNIE} ilosc_P2_W_to_M[w, 'M3']);

s.t. og20: m3_cost >= 18*m3_n;

# ograniczenia limitów produkcji wytwórni
s.t. produkcja_p1 {w in WYTWORNIE}:
    produkcja['P1', w] >= sum {m in MAGAZYNY} ilosc_P1_W_to_M[w, m];

s.t. prododukcja_p2 {w in WYTWORNIE}:
    produkcja['P2', w] >= sum {m in MAGAZYNY} ilosc_P2_W_to_M[w, m];

# ograniczenia równowagi węzłów-magazynów
s.t. rownowaga_p1 {m in MAGAZYNY}:
    sum {w in WYTWORNIE} ilosc_P1_W_to_M[w, m] = sum {s in SKLEPY} ilosc_P1_M_to_S[m, s];

s.t. rownowaga_p2 {m in MAGAZYNY}:
    sum {w in WYTWORNIE} ilosc_P2_W_to_M[w, m] = sum {s in SKLEPY} ilosc_P2_M_to_S[m, s];

# ograniczenia zapotrzebowania sklepów
s.t. zapotrzebowanie_p1 {s in SKLEPY}:
    zapotrzebowanie['P1', s] <= sum {m in MAGAZYNY} ilosc_P1_M_to_S[m, s];

s.t. zapotrzebowanie_p2 {s in SKLEPY}:
    zapotrzebowanie['P2', s] <= sum {m in MAGAZYNY} ilosc_P2_M_to_S[m, s];
