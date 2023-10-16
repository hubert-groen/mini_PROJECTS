import time
import gc
import random
import matplotlib as plt
import copy
import plotly.express as px
import pandas as pd
# include implemented algorithms
from trees.avl import AVL
from trees.bst import BST


def _time_benchmark(algorithm, array, preparation=None, preparation_array=None):
    if preparation is not None:
        preparation(preparation_array)
    gc_old = gc.isenabled()
    gc.disable()

    start_time = time.process_time()
    algorithm(array)
    stop_time = time.process_time()

    if gc_old:
        gc.enable()
    return stop_time - start_time


def creating_comparison(working_array, size):
    """
    simple function comapring time consumtion for
    creating trees
    """
    results = {}
    tree_alg = {
        'BST': BST().insert_list,
        'AVL': AVL().insert_list
    }
    for name, algorithm in tree_alg.items():
        test_array = copy.deepcopy(working_array[:size])

        results[name] = _time_benchmark(algorithm, test_array)

    return results


def searching_comparison(working_array, size):
    """
    simple function comapring time consumtion for
    searching in trees
    """

    results = {}
    bst_tree = BST()
    avl_tree = AVL()
    tree_alg = {
        'BST': [bst_tree.insert_list, bst_tree.search_list],
        'AVL': [avl_tree.insert_list, avl_tree.search_list]
    }
    MAX_LEGTH = 20000
    working_array = random.sample(range(1, 300000), MAX_LEGTH)
    for name, algorithm in tree_alg.items():
        test_array = copy.deepcopy(working_array[:size])
        results[name] = _time_benchmark(
            algorithm[1], test_array, preparation=algorithm[0], preparation_array=working_array)

    return results


def deleting_comparison(working_array, size):
    """
    simple function comapring time consumtion for
    searching in trees
    """

    results = {}
    bst_tree = BST()

    test_array = working_array[:size]
    results['BST'] = _time_benchmark(
        bst_tree.delete_list, test_array, preparation=bst_tree.insert_list, preparation_array=working_array)
    # for name, algorithm in tree_alg.items():
    #     test_array = copy.deepcopy(working_array[:size])
    #     results[name] = _time_benchmark(
    #         algorithm[1], test_array, preparation=algorithm[0], preparation_array=working_array)

    return results


def compare_diffrent_array_length(array_of_lengths=[1000, 2000, 5000, 10000], method=creating_comparison):

    results = {}
    MAX_LEGTH = 20000
    working_array = random.sample(range(1, 300000), MAX_LEGTH)

    for length in array_of_lengths:

        results[length] = method(working_array, length)

    return results


def get_plot(dict_data, names=None):
    df = _prepare_data_for_chart(dict_data, names=names)
    figure = px.line(df)
    figure.show()
    # plt.plot(dict_data.keys(),)


def _prepare_data_for_chart(dict_data, names=None):
    if names is not None:
        algorithms_names = names
    else:
        algorithms_names = ['BST', 'AVL']
    plot_data = {}
    for algorithm_name in algorithms_names:
        plot_data[algorithm_name] = []
        for _, score_dict in dict_data.items():
            plot_data[algorithm_name].append(score_dict[algorithm_name])

    return pd.DataFrame(plot_data, index=dict_data.keys())


if __name__ == '__main__':
    # data = _prepare_data_for_chart(compare_diffrent_array_length())
    # get_plot(compare_diffrent_array_length(
    #     method=deleting_comparison), names=['BST'])

    algorithm = BST().insert_list
    gc_old = gc.isenabled()
    gc.disable()
    MAX_LEGTH = 20000
    working_array = random.sample(range(1, 300000), 10000)

    start_time = time.process_time()
    algorithm(working_array)
    stop_time = time.process_time()

    if gc_old:
        gc.enable()
    print(stop_time - start_time)
    # print(pd.DataFrame(data, index=[100, 500, 1000, 2000]))
