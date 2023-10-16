import time
import gc
import copy
import plotly.express as px
import pandas as pd
from heaps.heap_mat import Heap
from heaps.heap_hub_smallup import HeapV
from heaps.heap_hub_smallup import draw_heap
from heaps.heap_hub_highup import HeapV_h
from heaps.heap_hub_highup import draw_heap_h
import random
import matplotlib.pyplot as plt

MAX_LENGTH = 100000


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


# def get_algorithms_comparison(array):
#     """
#     simple function comapring time consumtion for
#     all available sorting algorithms
#     """

#     results = {}

#     for name, algorithm in ALGORITHMS.items():
#         test_array = copy.deepcopy(array)
#         results[name] = _time_benchmark(algorithm, test_array)

#     return results


def creating_comparison(working_array, size):
    results = {}
    tree_alg = {
        'HEAP 2': Heap(2).insert_list,
        'HEAP 5': Heap(5).insert_list,
        'HEAP 7': Heap(7).insert_list
    }
    for name, algorithm in tree_alg.items():
        test_array = copy.deepcopy(working_array[:size])

        results[name] = _time_benchmark(algorithm, test_array)

    return results


def deleting_comparison(working_array, size):
    results = {}
    Heap2 = Heap(2)
    Heap5 = Heap(5)
    Heap7 = Heap(7)

    tree_alg = {
        'HEAP 2': [Heap2.delete_n, Heap2.insert_list],
        'HEAP 5': [Heap5.delete_n, Heap5.insert_list],
        'HEAP 7': [Heap7.delete_n, Heap7.insert_list]
    }
    for name, algorithm in tree_alg.items():
        test_array = copy.deepcopy(working_array[:size])

        results[name] = _time_benchmark(
            algorithm[0], size, algorithm[1], test_array)

    return results


def compare_diffrent_array_length(array_of_lengths=[100, 500, 1000, 2000], method=creating_comparison):
    original_array = random.sample(range(1, 300000), MAX_LENGTH)

    results = {}

    for length in array_of_lengths:
        test_array = copy.deepcopy(original_array)
        results[length] = method(test_array, length)

    return results


def get_plot(dict_data):
    df = _prepare_data_for_chart(dict_data)
    figure = px.line(df)
    figure.show()
    # plt.plot(dict_data.keys(),)


def _prepare_data_for_chart(dict_data):
    algorithms_names = ['HEAP 2', 'HEAP 5', 'HEAP 7']
    plot_data = {}
    for algorithm_name in algorithms_names:
        plot_data[algorithm_name] = []
        for _, score_dict in dict_data.items():
            plot_data[algorithm_name].append(score_dict[algorithm_name])

    return pd.DataFrame(plot_data, index=dict_data.keys())


def visualize_heap(degree):
    example_visualization = [31, 5, 10, 18, 14, 9, 6, 17, 1, 11]
    h = HeapV_h(degree)
    h.insert_list(example_visualization)
    draw_heap_h(h)


if __name__ == '__main__':
    # data = _prepare_data_for_chart(compare_diffrent_array_length())
    # get_plot(compare_diffrent_array_length(method=deleting_comparison))
    # print(pd.DataFrame(data, index=[100, 500, 1000, 2000]))

    visualize_heap(2)
    visualize_heap(5)
    visualize_heap(7)

    plt.show()
