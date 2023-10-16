import time
import gc
import matplotlib as plt
import copy
import plotly.express as px
import pandas as pd
# include implemented algorithms
from algorithms.naive import naive_search
from algorithms.KR import KR_search
from algorithms.KMP import KMP_search


from resources.get_resources import get_resources, get_resources_list


ALGORITHMS =\
    {
        'KMP': KMP_search,
        'KR': KR_search,
        'naive': naive_search,
    }


def _time_benchmark(algorithm, array, original_whole_text):
    gc_old = gc.isenabled()
    gc.disable()

    start_time = time.process_time()
    for word in array:
        algorithm(word, original_whole_text)
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
    original_whole_text = get_resources()

    for name, algorithm in ALGORITHMS.items():
        test_array = copy.deepcopy(array)
        results[name] = _time_benchmark(
            algorithm, test_array, original_whole_text)

    return results


def compare_diffrent_array_length(array_of_lengths=[100, 200, 500]):
    original_array = get_resources_list()

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
    get_plot(compare_diffrent_array_length([100, 200, 500, 700, 1000]))
