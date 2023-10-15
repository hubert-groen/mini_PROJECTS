import numpy as np
import matplotlib.pyplot as plt


def plot2D(function_dictionary, x_stack, y_stack):

    # f = fuction_dictionary['f']
    x_values = np.linspace(-2, 2, 1000)
    y_values = function_dictionary['f'](x_values)
    
    plt.plot(x_values, y_values)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('2D PLOT\ny(x)')
    plt.grid(True)

    plt.scatter(x_stack, y_stack, s=5, c='r', marker='o')

    plt.show()


def plot3D(function_dictionary, x1_stack, x2_stack, y_stack):

    # meshgrid
    x1 = np.linspace(-5, 5, 100)
    x2 = np.linspace(-5, 5, 100)
    X1, X2 = np.meshgrid(x1, x2)

    # values of the function for each (x1, x2) pair
    G = np.vectorize(function_dictionary['f'])(X1, X2)

    # 3D plot
    fig = plt.figure(figsize=(12,5))
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X1, X2, G, cmap='viridis')
    ax1.set_xlabel('X1')
    ax1.set_ylabel('X2')
    ax1.set_zlabel('Y')
    ax1.set_title('3D PLOT\ny(x1, x2)')

    ax1.scatter(x1_stack, x2_stack, y_stack, s=5, c='r', marker='o', zorder=2)
    
    # contour plot
    ax2 = fig.add_subplot(122)
    levels = np.linspace(np.min(G), np.max(G), 10)
    contours = ax2.contour(X1, X2, G, levels=levels, cmap='coolwarm')
    ax2.set_xlabel('X1')
    ax2.set_ylabel('X2')
    ax2.set_title('CONTOUR MAP\ny(x1, x2)')
    ax2.grid()

    ax2.scatter(x1_stack, x2_stack, s=5, c='r', marker='o')

    # displaying plots
    plt.show()