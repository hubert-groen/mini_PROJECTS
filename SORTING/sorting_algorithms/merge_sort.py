
def merge_sort(array):
    if (len(array)>1):
        r = len(array)//2
        left_half = array[:r]
        right_half = array[r:]

        merge_sort(left_half)
        merge_sort(right_half)

        left_arr_iterator=right_arr_iterator=main_arr_iterator=0

        while left_arr_iterator<len(left_half) and\
            right_arr_iterator<len(right_half):
            
            if(left_half[left_arr_iterator]< right_half[right_arr_iterator]):
                array[main_arr_iterator] = left_half[left_arr_iterator]
                left_arr_iterator += 1
            else:
                array[main_arr_iterator] = right_half[right_arr_iterator]
                right_arr_iterator += 1

            main_arr_iterator += 1
        
        #place remaining elements
        while left_arr_iterator < len(left_half):
            array[main_arr_iterator] = left_half[left_arr_iterator]
            left_arr_iterator += 1
            main_arr_iterator += 1
        
        while right_arr_iterator < len(right_half):
            array[main_arr_iterator] = right_half[right_arr_iterator]
            right_arr_iterator += 1
            main_arr_iterator += 1

if __name__ == '__main__':
    data = [8, 7, 2, 1, 2, 3, 14, 0, 9, 6]
    print("Unsorted Array")
    print(data)
    merge_sort(data)
    print('Sorted Array in Ascending Order:')
    print(data)