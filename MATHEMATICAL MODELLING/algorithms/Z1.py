import pulp

# Inicjalizacja problemu
problem = pulp.LpProblem("Minimalizacja_kosztow_transportu", pulp.LpMinimize)

# Zmienne decyzyjne (całkowite)
x_AD = pulp.LpVariable("x_AD", lowBound=0, cat=pulp.LpInteger)
x_BD = pulp.LpVariable("x_BD", lowBound=0, cat=pulp.LpInteger)
x_CD = pulp.LpVariable("x_CD", lowBound=0, cat=pulp.LpInteger)
x_AE = pulp.LpVariable("x_AE", lowBound=0, cat=pulp.LpInteger)
x_BE = pulp.LpVariable("x_BE", lowBound=0, cat=pulp.LpInteger)
x_CE = pulp.LpVariable("x_CE", lowBound=0, cat=pulp.LpInteger)

x_DE = pulp.LpVariable("x_DE", lowBound=0, cat=pulp.LpInteger)

x_DF = pulp.LpVariable("x_DF", lowBound=0, cat=pulp.LpInteger)
x_DG = pulp.LpVariable("x_DG", lowBound=0, cat=pulp.LpInteger)
x_DH = pulp.LpVariable("x_DH", lowBound=0, cat=pulp.LpInteger)
x_EF = pulp.LpVariable("x_EF", lowBound=0, cat=pulp.LpInteger)
x_EG = pulp.LpVariable("x_EG", lowBound=0, cat=pulp.LpInteger)
x_EH = pulp.LpVariable("x_EH", lowBound=0, cat=pulp.LpInteger)


# Funkcja celu
problem += (3*x_AD + 6*x_AE) + (6*x_BD + 3*x_BE) + (4*x_CD + 5*x_CE) + \
            2 * x_DE + \
           (5*x_DF + 5*x_EF) + (7*x_DG + 4*x_EG) + (3*x_DH + 2*x_EH), "Koszty_transportu"

# Ograniczenia
problem += x_AD + x_AE <= 10, "Ograniczenie_kopalni_A"
problem += x_BD + x_BE <= 13, "Ograniczenie_kopalni_B"
problem += x_CD + x_CE <= 22, "Ograniczenie_kopalni_C"

problem += x_DF + x_EF >= 15, "Zapotrzebowanie_elektrowni_F"
problem += x_DG + x_EG >= 10, "Zapotrzebowanie_elektrowni_G"
problem += x_DH + x_EH >= 10, "Zapotrzebowanie_elektrowni_H"

problem += x_AD <= 8
problem += x_AE <= 10
problem += x_BD <= 10
problem += x_BE <= 13
problem += x_CD <= 10
problem += x_CE <= 8

problem += x_DE <= 20

problem += x_DF <= 16
problem += x_EF <= 7
problem += x_DG <= 6
problem += x_EG <= 4
problem += x_DH <= 10
problem += x_EH <= 2

problem += (x_AD + x_BD + x_CD) - (x_DE + x_DF + x_DG + x_DH) == 0
problem += (x_AE + x_BE + x_CE + x_DE) - (x_EF + x_EG + x_EH) == 0


# Rozwiązanie problemu
problem.solve()

# Wyświetlenie wyników
for variable in problem.variables():
    print(f"{variable.name}: {int(variable.varValue)}")

print(f"Koszty transportu: {int(pulp.value(problem.objective))}")
