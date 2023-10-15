import time
import gc
import matplotlib as plt
import copy
import plotly.express as px
import pandas as pd 

from sorting_algorithms.bubble_sort import bubble_sort
from sorting_algorithms.insertion_sort import insertion_sort
from sorting_algorithms.merge_sort import merge_sort
from sorting_algorithms.quick_sort import quick_sort
from sorting_algorithms.selection_sort import selection_sort

from resources.get_resources import get_resources


ALGORITHMS =\
    {
        'bubble sort': bubble_sort,
        'insertion sort': insertion_sort,
        'merge sort': merge_sort,
        'quick sort': quick_sort,
        'selection sort': selection_sort,
    }

def _time_benchmark(algorithm, array):
    gc_old = gc.isenabled()
    gc.disable()
    
    start_time = time.process_time()
    algorithm(array)
    stop_time = time.process_time()

    if gc_old:
        gc.enable()
    
    return stop_time - start_time


def get_algorithms_comparison(array):
    """
    simple function comapring time consumtion for
    all available sorting algorithms
    """

    results = {}
    
    for name, algorithm in ALGORITHMS.items():
        test_array = copy.deepcopy(array)
        results[name] = _time_benchmark(algorithm, test_array)

    return results


def compare_diffrent_array_length(array_of_lengths=[100, 500, 1000, 2000]):
    original_array = get_resources()

    results = {}

    for length in array_of_lengths:
        test_array = copy.deepcopy(original_array[:length])
        results[length] = get_algorithms_comparison(test_array)

    return results

def get_plot(dict_data):
    df = _prepare_data_for_chart(dict_data)
    figure = px.line(df)
    figure.show()
    # plt.plot(dict_data.keys(),)

def _prepare_data_for_chart(dict_data):
    algorithms_names = ALGORITHMS.keys()
    plot_data = {}
    for algorithm_name in algorithms_names:
        plot_data[algorithm_name] = []
        for _, score_dict in dict_data.items():
            plot_data[algorithm_name].append(score_dict[algorithm_name])
    
    return pd.DataFrame(plot_data, index=dict_data.keys())

if __name__ == '__main__':
    get_plot(compare_diffrent_array_length())

