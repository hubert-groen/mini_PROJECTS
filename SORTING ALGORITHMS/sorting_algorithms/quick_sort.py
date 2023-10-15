
def quick_sort(array):
    """Implementation of quick sort algorithm"""
    first_index = 0
    last_index = len(array)-1
    _quick_sort_recursion_helper(array, first_index, last_index)


def _quick_sort_recursion_helper(array, start_index,  stop_index):

    if (start_index < stop_index):
        partitoning_index = _partition(array, start_index, stop_index)

        # left side sorting
        _quick_sort_recursion_helper(array, start_index, partitoning_index-1)

        # right side sorting
        _quick_sort_recursion_helper(array, partitoning_index+1, stop_index)


def _partition(array,  start_index,  stop_index):
    pivot_element = array[stop_index]

    # index of element which value is greater than pivot
    greater_element_index = start_index

    for current_index in range(start_index, stop_index):
        if (array[current_index] <= pivot_element):

            # swapping current element with element greater than pivot
            (array[greater_element_index], array[current_index]) =\
                (array[current_index], array[greater_element_index])

            greater_element_index += 1


    # final swap of pivot with greater element
    (array[greater_element_index], array[stop_index]) =\
        (array[stop_index], array[greater_element_index])

    return greater_element_index


if __name__ == '__main__':
    data = [8, 7, 2, 1, 2, 3, 14, 0, 9, 6]
    print("Unsorted Array")
    print(data)
    quick_sort(data)
    print('Sorted Array in Ascending Order:')
    print(data)