'''
https://www.crio.do/blog/data-structures-interview-questions/

1.  + Trapping Rainwater
2.  ? Rat in a Maze
3.  + House Robber
4.  + Merge K sorted linked lists
5.  + Valid parentheses
6.  + Search a 2D Matrix
7.  ? Number of Islands
8.  - Merge Intervals
9.  - Minimize Cash Flow
10. - LRU Cache

11. + Morse alphabet

'''

#   1
def trapping_rainwater(arr): 
  
    res = 0

    for i in range(1, len(arr) - 1):

        left = arr[i] 
        for j in range(i): 
            left = max(left, arr[j]) 

        right = arr[i]
        for j in range(i + 1, len(arr)): 
            right = max(right, arr[j]) 

        res = res + (min(left, right) - arr[i])

    return res

# region
# arr = [3,0,2,0,4]
# print(trapping_rainwater(arr))
# endregion

# similar task from leetcode
def water_containter(height):

    area_record = 0

    lower_index = 0
    higher_index = len(height) - 1

    while lower_index != higher_index:

        current_area = (higher_index - lower_index) * min(height[lower_index], height[higher_index])

        area_record = max(area_record, current_area)

        if height[lower_index] >= height[higher_index]:
            higher_index -= 1
        else:
            lower_index += 1

    return area_record

# region
# arr = [1,8,6,2,5,4,8,3,7]
# print(water_containter(arr))
# endregion



#   2
#   TODO: wyświetla się albo jedna ścieżka, albo są powielone
class ListNode:
    def __init__(self, val = 0, prev = None):
        self.val = val
        self.prev = prev

def maze(matrix):

    def is_valid(row, col):

        if row < 0 or col < 0:
            return False
        elif row > len(matrix)-1 or col > len(matrix[0])-1:
            return False
        elif matrix[row][col] == 0:
            return False
        else:
            return True

    def get_neighbours(parent):

        neighbours = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        d = 1
        for dir in directions:

            row = parent.val[0] + dir[0]
            col = parent.val[1] + dir[1]

            if is_valid(row, col):

                if (row, col) not in visited or d < 3:              # TODO: zmienić jakoś to d < 3
                    new_node = ListNode((row, col), parent)
                    neighbours.append(new_node)
                    visited.append((row, col))
            
            d += 1

        return neighbours
      
    start_point = ListNode((0,0))
    next_nodes = []
    next_nodes.append(start_point)
    visited = []

    output = []

    while len(next_nodes) > 0:
        top = next_nodes[-1]
        next_nodes.pop()

        print(f"now get_nei for {top.val}")
        new_neighbours = get_neighbours(top)

        for i in new_neighbours:
            next_nodes.append(i)

            if i.val == (3,3):
                output.append(i)
                break

    return output

# region
# M = [[1,0,0,0],
#      [1,1,1,1],
#      [1,1,0,1],
#      [0,1,1,1]]

# result = maze(M)

# for k in range(len(result)):

#     # empty output matrix
#     output_matrix = [[0 for _ in range(4)] for _ in range(4)]
#     output_matrix[0][0] = 1

#     # backpropagating the path
#     current = result[k]
#     while current.prev is not None:
#         output_matrix[current.val[0]][current.val[1]] = 1
#         current = current.prev

#     for row in output_matrix:
#         print(row)

#     print('\n')
# endregion



#   3
def house_robber(nums):
    if len(nums) < 2:
        return max(nums)

    steak = [0] * (len(nums))

    steak[0] = nums[0]
    steak[1] = max(nums[0] , nums[1])

    for house in range(2, len(nums)):
        steak[house] = max(steak[house-2]+nums[house] , steak[house-1])

    return steak[-1]  

# region
# hval = [6,7,1,3,8,2,4]
# print(house_robber(hval))
# endregion



#   4
#   TODO: done on leetcode, but increase efficiency



#   5
def valid_parentheses(s):

    if len(s) % 2 != 0:
        return False

    d = {')': '(', ']': '[', '}': '{'}

    stack = []

    for i in s:
        if i not in d:
            stack.append(i)
        else:
            if len(stack) != 0 and d[i] == stack[-1]:
                stack.pop()
            else:
                return False
    
    if len(stack) == 0:
        return True
    else:
        return False

# region
# s = "()[]{}"
# print(valid_parentheses(s))
# endregion


#   6
def search_2D_matrix(matrix, target):

    rows = len(matrix)
    cols = len(matrix[0])

    left = 0
    right = rows*cols - 1


    while left <= right:

        mid = (left + right) // 2
        mid_value = matrix[mid // cols][mid % rows]

        if mid_value < target:
            left = mid + 1
        elif mid_value > target:
            right = mid + 1
        else:
            return (mid // cols, mid % rows)
    
    return False

# region
# mat = [[ 1,  5,  9,  11,  13],
#        [14, 20, 21,  26,  28],
#        [30, 34, 43,  50,  55],
#        [57, 69, 77,  81,  83],
#        [90, 92, 99, 101, 110]]

# target = 110

# print(search_2D_matrix(mat, target))
# endregion



#   7
#   TODO: na leetcode nie przeszło, bo za duży timeout
def number_of_islands(mat):

    def is_valid(row, col):

        if row < 0 or col < 0:
            return False
        elif row > len(mat)-1 or col > len(mat[0])-1:
            return False
        else:
            return True

    def check_neighbours(row, col):

        # directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
        #               (1, 1), (-1,-1), (1,-1), (-1, 1)]

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        found_ones = 0
        
        for dir in directions:

            r = row + dir[0]
            c = col + dir[1]

            if is_valid(r, c) and (r, c) not in visited:

                visited.append((r, c))

                if mat[r][c] == 1:
                    found_ones += 1
                    check_neighbours(r, c)

        return found_ones
        
    visited = []
    islands = 0

    for row_i in range(len(mat)):
        for col_i in range(len(mat[0])):

            if mat[row_i][col_i] == 1 and (row_i, col_i) not in visited:
                islands += 1
                check_neighbours(row_i, col_i)

    return islands

# region
# matrix = [  [1,1,0,0,0],
#             [1,1,0,0,0],
#             [0,0,0,1,0],
#             [1,0,0,1,0]]

# matrix2 = [ [1,1,1,1,0],
#             [1,1,0,1,0],
#             [1,1,0,0,0],
#             [0,0,0,0,0]]

# matrix3 = [ [1,1,0,0,0],
#             [1,1,0,0,0],
#             [0,0,1,0,0],
#             [0,0,0,1,1]]

# print(number_of_islands(matrix3))
# endregion



#   11
# requires proper text file in the folder
def morse(file_name):

    DICTIONARY = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',}

    with open(f'{file_name}.txt', 'r') as file:                    # 'r' stand for reading mode

        for line in file:
            line = line.upper()                             # every letter is set to 
            new = ''

            for n in range(len(line)):

                if line[n] in DICTIONARY:                   # if given letter exist in the dictionary
                    new += DICTIONARY[line[n]] + ' '

                elif(line[n] == ' ' and new[-2] != '/'):    # space sign + check if there are no 2 consecutive spaces
                    new += '/ '

                elif(line[n] == '\n'):                      # if end of line, go to reading the next one
                    break

                else:                                       # if there is not known letter, space or endline it means we deal with unknown character (not included it dictionary)
                    continue                                # then go to the next letter
                
            print(new)                                      # printing line by line

# region
# morse('text_to_morse')
# endregion