import pulp

# Inicjalizacja problemu
problem = pulp.LpProblem("Minimalizacja_odchylen", pulp.LpMinimize)

# Zmienne decyzyjne
x = [pulp.LpVariable(f"x_{i}", lowBound=0) for i in range(8)]

# Plan bazowy
plan_bazowy = [240, 385, 138, 224, 144, 460, 198, 200]

# Względne odchylenia
wzg_odchylenia = [pulp.LpVariable(f"odchylenie_{i}", lowBound=0) for i in range(8)]

# Maksymalne względne odchylenie
max_odchylenie = pulp.LpVariable("max_odchylenie", lowBound=0)

# Funkcja celu: minimalizacja sumy maksymalnego odchylenia i sumy wszystkich odchyleń
problem += max_odchylenie + pulp.lpSum(wzg_odchylenia), "Minimalizacja_odchylen"

# Ograniczenia
problem += x[0] + x[2] + x[7] >= 1.12 * (plan_bazowy[0] + plan_bazowy[2] + plan_bazowy[7])
problem += x[2] + x[4] <= 0.93 * (plan_bazowy[2] + plan_bazowy[4])
problem += x[2] >= 0.8 * x[6]

# Sumaryczna wielkość sprzedaży nie zmienia się
problem += pulp.lpSum(x) == pulp.lpSum(plan_bazowy)

# Obliczanie względnych odchyleń
for i in range(8):
    problem += wzg_odchylenia[i] == (x[i] - plan_bazowy[i]) / plan_bazowy[i]

# Maksymalne odchylenie
problem += max_odchylenie >= pulp.lpSum(wzg_odchylenia)

# Rozwiązanie problemu
problem.solve()

# Wyświetlenie wyników
for i, variable in enumerate(x):
    print(f"x_{i+1}: {int(variable.varValue)}")

print(f"Maksymalne odchylenie: {int(max_odchylenie.varValue)}")
