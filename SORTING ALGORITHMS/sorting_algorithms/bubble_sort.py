def bubble_sort(array):

    for m in range(len(array)-1, 0, -1):

        for n in range(m):

            if array[n] > array[n+1]:
            
                array[n], array[n+1] = array[n+1], array[n]
                
    return array