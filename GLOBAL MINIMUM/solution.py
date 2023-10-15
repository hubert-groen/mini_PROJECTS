from math import exp
from visualization import plot2D
from visualization import plot3D


class GradientDescent():
    
    def __init__(self, learn_rate = 0.2, precision = 0.001, max_steps = 10000):
        self.learning_rate = learn_rate
        self.precision = precision
        self.max_steps = max_steps

    def get_parameters(self):
        return {
            "learn_rate": self.learning_rate,
            "precision": self.precision,
            "max_steps": self.max_steps
        }

    def solve(self, df, x1, x2 = None):

        if (x2 == None):
            x_stack = []
            x_stack.append(x1)
            y_stack = []
            y_stack.append(df['f'](x_stack[-1]))
            previous_step_size = 1
            it_counter = 0
        
            while previous_step_size > self.precision and it_counter < self.max_steps:

                previous_x = x_stack[-1]

                dfdx = df['dfdx'](x_stack[-1])

                x_stack.append(x_stack[-1] - self.learning_rate * dfdx)
                y_stack.append(df['f'](x_stack[-1]))

                previous_step_size = abs(x_stack[-1] - previous_x)
                it_counter += 1

                print("Iteration {}: {}".format(it_counter, previous_x))

            return x_stack, y_stack, it_counter

        elif (x2 != None):
            x1_stack = []
            x1_stack.append(x1)
            x2_stack = []
            x2_stack.append(x2)
            y_stack = []
            y_stack.append(df['f'](x1_stack[-1], x2_stack[-1]))
            previous_step_size_x1 = 1
            previous_step_size_x2 = 1
            it_counter = 0

            while (previous_step_size_x1 > self.precision and previous_step_size_x2 > self.precision) and it_counter < self.max_steps:

                previous_x1 = x1_stack[-1]
                previous_x2 = x2_stack[-1]

                dgdx1 = df['dfdx1'](x1_stack[-1], x2_stack[-1])
                dgdx2 = df['dfdx2'](x1_stack[-1], x2_stack[-1])

                x1_stack.append(x1_stack[-1] - self.learning_rate * dgdx1)
                x2_stack.append(x2_stack[-1] - self.learning_rate * dgdx2)
                y_stack.append(df['f'](x1_stack[-1], x2_stack[-1]))

                previous_step_size_x1 = abs(x1_stack[-1] - previous_x1)
                previous_step_size_x2 = abs(x2_stack[-1] - previous_x2)
                it_counter += 1

                # print("Iteration " + str(it_counter) + ": (" + str(x1_stack[-1]) + ", " + str(x2_stack[-1]) + ")")

            return x1_stack, x2_stack, y_stack, it_counter
    

def main():

    function_2D = {
        'f' : lambda x: 2*x**2 + 3*x + 1,
        'dfdx' : lambda x: 4*x + 3
    }

    function_2Da = {
        'f' : lambda x: x**4 - 4*x**2 + x + 4,
        'dfdx' : lambda x: 4*x**3 - 8*x + 1
    }

    function_3D = {
        'f' : lambda x1, x2: 1-0.6*exp(-x1**2 - x2**2) - 0.4*exp(-(x1+1.75)**2 - (x2-1)**2), 
        'dfdx1': lambda x1, x2: 1.2*x1*exp(-x1**2 - x2**2) + 0.8*(x1+1.75)*exp(-(x1+1.75)**2 - (x2-1)**2),
        'dfdx2': lambda x1, x2: 1.2*x2*exp(-x1**2 - x2**2) + 0.8*(x2-1)*exp(-(x1+1.75)**2 - (x2-1)**2)
    }

        # starting points
    
    x1_initial = -2
    x2_initial = 2

        # 2D - SOLUTION
    # gd_f = GradientDescent()
    # result_f = gd_f.solve(function_2D, x1_initial)
    # print("\nRESULTS SUMMARY FOR f(x):")
    # print("x_initial:   " + str(x1_initial))
    # print("x_final:     " + str(result_f[0][-1]))
    # print("iterations:  " + str(result_f[2]) + "\n")
    # plot2D(function_2D, result_f[0], result_f[1])

        # 3D - SOLUTION
    gd_g = GradientDescent()
    result_g = gd_g.solve(function_3D, x1_initial, x2_initial)
    print("\nRESULTS SUMMARY FOR g(x):")
    print("x_initial:  (" + str(x1_initial) + ", " + str(x2_initial) + ")")
    print("x_final:    (" + str(result_g[0][-1]) + ", " + str(result_g[1][-1]) + ")")
    print("iterations:  " + str(result_g[3]) + "\n")
    plot3D(function_3D, result_g[0], result_g[1], result_g[2])


if __name__ == "__main__":
    main()