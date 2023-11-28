
# JEDNO OPTYMALNE ROZWIĄZANIE
# region
import pulp

# Inicjalizacja problemu
problem = pulp.LpProblem("Minimalizacja_kosztow_transportu", pulp.LpMinimize)

# Zmienne decyzyjne (całkowite)
x_A1 = pulp.LpVariable("x_A1", lowBound=0, cat=pulp.LpInteger)
x_A3 = pulp.LpVariable("x_A3", lowBound=0, cat=pulp.LpInteger)
x_A5 = pulp.LpVariable("x_A5", lowBound=0, cat=pulp.LpInteger)
x_A6 = pulp.LpVariable("x_A6", lowBound=0, cat=pulp.LpInteger)

x_B2 = pulp.LpVariable("x_B2", lowBound=0, cat=pulp.LpInteger)
x_B3 = pulp.LpVariable("x_B3", lowBound=0, cat=pulp.LpInteger)
x_B4 = pulp.LpVariable("x_B4", lowBound=0, cat=pulp.LpInteger)

x_C1 = pulp.LpVariable("x_C1", lowBound=0, cat=pulp.LpInteger)
x_C2 = pulp.LpVariable("x_C2", lowBound=0, cat=pulp.LpInteger)
x_C4 = pulp.LpVariable("x_C4", lowBound=0, cat=pulp.LpInteger)
x_C5 = pulp.LpVariable("x_C5", lowBound=0, cat=pulp.LpInteger)

x_D1 = pulp.LpVariable("x_D1", lowBound=0, cat=pulp.LpInteger)
x_D3 = pulp.LpVariable("x_D3", lowBound=0, cat=pulp.LpInteger)
x_D5 = pulp.LpVariable("x_D5", lowBound=0, cat=pulp.LpInteger)

x_E2 = pulp.LpVariable("x_E2", lowBound=0, cat=pulp.LpInteger)
x_E4 = pulp.LpVariable("x_E4", lowBound=0, cat=pulp.LpInteger)
x_E6 = pulp.LpVariable("x_E6", lowBound=0, cat=pulp.LpInteger)

x_F1 = pulp.LpVariable("x_F1", lowBound=0, cat=pulp.LpInteger)
x_F5 = pulp.LpVariable("x_F5", lowBound=0, cat=pulp.LpInteger)
x_F6 = pulp.LpVariable("x_F6", lowBound=0, cat=pulp.LpInteger)


# Funkcja celu
problem += (x_A1 + x_A3 + x_A5 + x_A6) + (x_B2 + x_B3 + x_B4) + (x_C1 + x_C2 + x_C4 + x_C5) + \
           (x_D1 + x_D3 + x_D5) + (x_E2 + x_E4 + x_E6) + (x_F1 + x_F5 + x_F6), "Koszty_transportu"


# Ograniczenia
problem += (x_A1 + x_A3 + x_A5 + x_A6) == 1
problem += (x_B2 + x_B3 + x_B4) == 1
problem += (x_C1 + x_C2 + x_C4 + x_C5) == 1
problem += (x_D1 + x_D3 + x_D5) == 1
problem += (x_E2 + x_E4 + x_E6) == 1
problem += (x_F1 + x_F5 + x_F6) == 1

problem += (x_A1 + x_C1 + x_D1 + x_F1) == 1
problem += (x_B2 + x_C2 + x_E2) == 1
problem += (x_A3 + x_B3 + x_D3) == 1
problem += (x_B4 + x_C4 + x_E4) == 1
problem += (x_A5 + x_C5 + x_D5 + x_F5) == 1
problem += (x_A6 + x_E6 + x_F6) == 1



# Rozwiązanie problemu
problem.solve()

# Wyświetlenie wyników
for variable in problem.variables():
    print(f"{variable.name}: {int(variable.varValue)}")

print(f"Koszty transportu: {int(pulp.value(problem.objective))}")
# endregion


# WSZYSTKIE OPTYMALNE ROZWIĄZANIA
# region
# import itertools

# zespoły = ['A', 'B', 'C', 'D', 'E', 'F']
# projekty = [1, 2, 3, 4, 5, 6]

# kompetencje = {
#     1: ['A', 'C', 'D', 'F'],
#     2: ['B', 'C', 'E'],
#     3: ['A', 'B', 'D'],
#     4: ['B', 'C', 'E'],
#     5: ['A', 'C', 'D', 'F'],
#     6: ['A', 'E', 'F']
# }

# def is_valid_assignment(assignment):
#     for projekt, zespół in assignment.items():
#         if zespół not in kompetencje[projekt]:
#             return False
#     return True

# def find_all_assignments(zespoły, projekty):
#     all_assignments = []
#     for assignment in itertools.permutations(zespoły, len(projekty)):
#         assignment_dict = dict(zip(projekty, assignment))
#         if is_valid_assignment(assignment_dict):
#             all_assignments.append(assignment_dict)
#     return all_assignments

# assignments = find_all_assignments(zespoły, projekty)

# i = 1
# for assignment in assignments:
#     print(f"Możliwy przydział nr {i}:")
#     for projekt, zespół in assignment.items():
#         print(f"Projekt {projekt} -> Zespół {zespół}")
#     print()
#     i += 1

# endregion