import matplotlib.pyplot as plt
import numpy as np


# PLOT FOR 1 SET OF VALUES
def plot_best(best_stacks):

    num_iterations = len(best_stacks[0])

    # Calculate the best, worst, and average values for each iteration across all stacks
    best_values = [max([stack[i] for stack in best_stacks]) for i in range(num_iterations)]
    worst_values = [min([stack[i] for stack in best_stacks]) for i in range(num_iterations)]
    avg_values = [np.mean([stack[i] for stack in best_stacks]) for i in range(num_iterations)]

    # Plot the best, worst, and average lines
    plt.plot(range(num_iterations), best_values, label='Best run')
    plt.plot(range(num_iterations), worst_values, label='Worst run')
    plt.plot(range(num_iterations), avg_values, linestyle='--', label='Average run')

    # Fill the area between the best and worst lines
    plt.fill_between(range(num_iterations), best_values, worst_values, alpha=0.2)

    plt.xlabel('Iterations')
    plt.ylabel('Best value')
    plt.title(r'$\mathbf{Best\ value\ improvement}$'+'\n'+'results for 25 runs of the algorithm')
    plt.legend()

    # plt.show()

# PLOT AVERAGE VALUES FOR DIFFERENT PC
def plot_averages(average_stacks, max_iterations=20):
    fig, ax = plt.subplots()
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Best value')
    plt.title(r'$\mathbf{Best\ value\ improvement}$'+'\n'+'for different pc')

    labels = ['pc=0.1', 'pc=0.25', 'pc=0.5', 'pc=0.75', 'pc=0.85']
    for i, best_stack in enumerate(average_stacks[:5]):
        ax.plot(np.linspace(0, max_iterations, len(best_stack)), best_stack, label=labels[i])

    for i, best_stack in enumerate(average_stacks[5:]):
        ax.plot(np.linspace(0, max_iterations, len(best_stack[:max_iterations])), best_stack[:max_iterations], '--')

    ax.legend()

