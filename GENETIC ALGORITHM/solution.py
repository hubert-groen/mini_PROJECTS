import random
import time
import numpy as np
import matplotlib.pyplot as plt
from visualization import plot_best
from visualization import plot_averages


class GeneticAlgorithm:

    def __init__(self, individuals_number = 400, iterations = 500, pc = 0.85, pm = 0.15):
        self.individuals_number = individuals_number
        self.iterations = iterations
        self.pc = pc
        self.pm = pm
    
    def drone_simulation(self, X):
        T = 100
        g = -10
        dt = 0.1
        P = 30
        r = 0.1
        v_crash = 20
        crash_penalty = 1500

        h = 0
        v = 0
        t = 0

        max_h = 0


        while h >= 0:
            if t < T:
                a = g + P * X[t] - v * r
                v += a * dt
                h += v * dt
            else:
                a = g - v * r 
                v += a * dt
                h += v * dt

            t += 1

            max_h = max(h, max_h)
        
        reward = max_h
        if v < -v_crash:
            reward -= crash_penalty

        return round(reward, 2)

    def initial_population(self):
        population = []
        number_of_bits = 100        # same as T in drone_function

        for _ in range(self.individuals_number):
            individual = [random.randint(0, 1) for _ in range(number_of_bits)]
            population.append(individual)

        return population

    def roulette(self, population, values):

        min_values = min(values)

        for m in range(len(values)):          # oceny zostały podniesione o wartość bezwzględną najwyższego + 1
            values[m] += (min_values + 1)     # aby nie przeprowadzać losowania statystycznego na liczbach <= 0


        values_sum = sum(values)
        probabilities = [k / values_sum for k in values]  # obliczenie prawdopodobieństw wyboru każdego osobnika

        parents = []

        for i in range(self.individuals_number):
            r = random.uniform(0, 1)                      # losowanie liczby z przedziału [0, 1)
            cumulative_prob = 0

            for j, prob in enumerate(probabilities):      # zwracanie indeksu oraz wartości elementów w tabeli
                cumulative_prob += prob

                if r <= cumulative_prob:                  # kiedy wartość "cumulative_prob" jest >= wylosowanemu "r" [0,1]
                    parents.append(population[j])         # osobnik o indeksie "j" zostaje wybrany do populacji
                    break

        return parents

    def crossover(self, population):
        kr_population = []

        for i in range(0, len(population) - 1, 2):
            parent1 = population[i]
            parent2 = population[i+1]

            # jeśli wylosowana liczba < "ps", to robimy krzyżowanie
            if random.uniform(0, 1) < self.pc:
                crossover_point = random.randint(1, len(parent1)-1)
                child1 = parent1[:crossover_point] + parent2[crossover_point:]
                child2 = parent2[:crossover_point] + parent1[crossover_point:]
            
            # jeśli krzyżowanie nie zachodzi, to klonujemy rodziców
            else:            
                child1 = parent1[:]
                child2 = parent2[:]

            kr_population.append(child1)
            kr_population.append(child2)

        return kr_population

    def mutation(self, population):

        for i in range(len(population)):
            for j in range(len(population[i])):
                if random.uniform(0, 1) < self.pm:
                    population[i][j] = 1 - population[i][j]          # zmiana bitu: 0-1 lub 1-0

        return population

    def run_algorithm(self):
        init_population = self.initial_population()

        # NADANIE WARTOŚCI PIERWSZEJ POPULACJI - dla każdego osobnika
        init_values = []
        for individual in init_population:
            reward = self.drone_simulation(individual)
            init_values.append(reward)

        # ZNALEZIENIE OSOBNIKA Z NAJWIĘKSZĄ OCENĄ + ZAPAMIĘTANIE WARTOŚCI OCENY NA STOSIE
        X_best = init_population[init_values.index(max(init_values))]
        V_best = max(init_values)
        stack_of_best = []
        stack_of_best.append(V_best)

        # utworzenie kopii, na których będzie iterował algorytm
        next_population = init_population.copy()
        next_values = init_values.copy()

        print("\nBest initial = " + str(V_best))
        print("-------------------")

        # ITERACJE ALGORYTMU
        for i in range(self.iterations):
            R = self.roulette(next_population, next_values)
            C = self.crossover(R)
            M = self.mutation(C)

            # wyzerowanie tablicy ocen i nadanie nowych wartości po nowej iteracji
            next_values = []
            for k in M:
                reward = self.drone_simulation(k)
                next_values.append(reward)

            # sprawdzenie czy mamy nowego osobnika z wyższą oceną niż obecny max
            temp_V_best = max(next_values)
            index_temp_V_best = next_values.index(temp_V_best)
            temp_X_best = M[index_temp_V_best]

            if (temp_V_best > V_best):
                print("Best was updated in " + str(i + 1) + " iteration! " + str(V_best) + " ----> " + str(temp_V_best) + "\n")
                X_best = temp_X_best
                V_best = temp_V_best

            stack_of_best.append(V_best)

            next_population = M

        # PODSUMOWANIE
        print("\n----- PODSUMOWANIE ------")
        print("Best overal =  " + str(V_best) + "\n")

        return stack_of_best


def main():

    start_time = time.time()
    average_stacks = []

    #####   A1  pc=0.75   #####
    a1 = []
    for i in range(5):
        a1.append(GeneticAlgorithm(10, 20, 0.75, 0.1))

    a1_best_values = []
    for k in a1:
        a1_best_values.append(k.run_algorithm())

    a1_avg_values = [np.mean([stack[i] for stack in a1_best_values]) for i in range(len(a1_best_values))]

    plot_best(a1_best_values)


    # TESTY DLA RÓŻNYCH PC
    # region
    #####   A2  pc=0.10   #####
    a2 = []
    for i in range(5):
        a2.append(GeneticAlgorithm(10, 20, 0.1, 0.1))

    a2_best_values = []
    for k in a2:
        a2_best_values.append(k.run_algorithm())

    a2_avg_values = [np.mean([stack[i] for stack in a2_best_values]) for i in range(len(a2_best_values))]
    average_stacks.append(a2_avg_values)


    #####   A3  pc=0.25   #####
    a3 = []
    for i in range(5):
        a3.append(GeneticAlgorithm(10, 20, 0.25, 0.1))
    
    a3_best_values = []
    for k in a3:
        a3_best_values.append(k.run_algorithm())

    a3_avg_values = [np.mean([stack[i] for stack in a3_best_values]) for i in range(len(a3_best_values))]
    average_stacks.append(a3_avg_values)


    #####   A4  pc=0.50   #####
    a4 = []
    for i in range(5):
        a4.append(GeneticAlgorithm(10, 20, 0.5, 0.1))

    a4_best_values = []
    for k in a4:
        a4_best_values.append(k.run_algorithm())

    a4_avg_values = [np.mean([stack[i] for stack in a4_best_values]) for i in range(len(a4_best_values))]
    average_stacks.append(a4_avg_values)
    average_stacks.append(a1_avg_values)


    #####   A5  pc=0.85   #####
    a5 = []
    for i in range(5):
        a5.append(GeneticAlgorithm(10, 20, 0.85, 0.1))

    a5_best_values = []
    for k in a5:
        a5_best_values.append(k.run_algorithm())

    a5_avg_values = [np.mean([stack[i] for stack in a5_best_values]) for i in range(len(a5_best_values))]
    average_stacks.append(a5_avg_values)

    plot_averages(average_stacks, 20)
    # endregion

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken:.6f} seconds")

    plt.show()


if __name__ == "__main__":
    main()
