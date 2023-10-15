def insertion_sort(u):

    for i in range(1, len(u)):
        temp = u[i]
        j = i - 1

        while j >= 0 and u[j] > temp:
            u[j + 1] = u[j]
            j -= 1
        u[j + 1] = temp

    return u