from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from classifier import Medical_classifier


def plot_accuracy(ta, va, depth):
    t_plot = [np.mean(ta[depth]) for depth in range(depth)]
    v_plot = [np.mean(va[depth]) for depth in range(depth)]

    best_depth = max(v_plot)
    best_depth_index = v_plot.index(best_depth) + 1
    
    plt.plot(np.arange(1, depth + 1), t_plot, color='blue', label='TRAINING SET')
    plt.plot(np.arange(1, depth + 1), v_plot, color='green', label='VALIDATION SET')
    plt.scatter(best_depth_index, best_depth, color='red', marker='o')
    plt.title('ACCURACY OVER DEPTH')
    plt.ylabel('accuracy')
    plt.xlabel('depth of ID3 tree')
    plt.legend(loc='upper left')
    # plt.show()


def main():

    data_path = 'cardio_train.csv'
    klasa = 'cardio'

    solver = Medical_classifier(data_path, klasa)
    solver.manage_data()                              # dyskretyzacja i podział na zbiory: train, validate, test


    # WPŁYW GŁĘBOKOŚCI NA DOKŁADNOŚĆ PREDYKCJI
    # region
    tree_depth = solver.max_tree_depth

    accuracies = {}
    best_validation_accuracy = 0
    best_depth = None

    print("\nAccuracies for ID3 trees with increasing depths:")
    print("D - depth")
    print("T - training set accuracy")
    print("V - validation set accuracy\n")

    for depth in range(tree_depth):

        accuracies[depth] = {}
        solver.change_depth(depth)

        ID3_tree = {}
        solver.ID3(ID3_tree, None, True, 0, pd.concat([solver.X_train, solver.Y_train], axis=1))
        solver.add_tree(ID3_tree)

        train_accuracy = solver.prediction_accuracy(solver.X_train, solver.Y_train)
        validation_accuracy = solver.prediction_accuracy(solver.X_val, solver.Y_val)

        if validation_accuracy > best_validation_accuracy:
            best_depth = depth + 1

        print("-----------------")
        print("D = " + str(depth+1))
        print("T = " + str(round(train_accuracy,3)))
        print("V = " + str(round(validation_accuracy,3)))
        print("-----------------")

        accuracies[depth]["T"] = train_accuracy
        accuracies[depth]["V"] = validation_accuracy

    train_values = [accuracies[i]["T"] for i in range(tree_depth)]
    validation_values = [accuracies[i]["V"] for i in range(tree_depth)]

    TA = {depth: [train_values[depth]] for depth in range(tree_depth)}
    VA = {depth: [validation_values[depth]] for depth in range(tree_depth)}

    plot_accuracy(TA, VA, tree_depth)
    # endregion
    

    # TESTOWANIE (na najlepszej głębokości)
    # region
    solver.change_depth(best_depth)

    new_ID3_tree = {}
    solver.ID3(new_ID3_tree, None, True, 0, pd.concat([solver.X_train, solver.Y_train], axis=1))
    solver.add_tree(new_ID3_tree)

    test_accuracy = solver.prediction_accuracy(solver.X_test, solver.Y_test)

    
    print("\n-----------------------------------\n")
    print("TEST SET ACCURACY:")
    print("For best depth = " + str(best_depth) + ", prediction accuracy = " + str(round(test_accuracy, 3)))
    print("\n-----------------------------------\n")
    # endregion


    plt.show()


if __name__ == '__main__':
    main()

