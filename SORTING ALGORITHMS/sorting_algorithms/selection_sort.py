def selection_sort(array):

    n = len(array)
    for i in range(n):
        minimum = i

        for k in range(i+1, n):
        
            if array[k] < array[minimum]:
                minimum = k

        array[i], array[minimum] = array[minimum], array[i]

    return array