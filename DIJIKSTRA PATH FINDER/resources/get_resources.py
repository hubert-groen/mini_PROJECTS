import os

DIRNAME = os.path.dirname(__file__)

# def get_resources(filename = 'example.txt'):
#     FILENAME = os.path.join(DIRNAME, filename )
#     output = []
#     with open(FILENAME, mode='r') as file:
#         lines = file.readlines()
#         # longest_line = max(lines, key=len)
#         # print('Longest line: ', longest_line, 'size: ', len(longest_line))
#         # columns = len(longest_line)
        
#         for line in lines:
#             line_element = []
#             for char in line:
#                 if(char == '\n'):
#                     continue
#                 line_element.append(char)
#             print(line_element)
#             output.append(line_element)
#     return output
    
def get_resources(filename = 'example_3.txt'):
    FILENAME = os.path.join(DIRNAME, filename )
    output = []

    start = None
    end = None

    with open(FILENAME, mode='r') as file:
        lines = file.readlines()

        x_coord = 0
        
        for line in lines:

            y_coord = 0

            line_element = []
            for char in line:

                if (start is not None and char == "X"):
                    end = [x_coord, y_coord]

                if (start is None and char == "X"):
                    start = [x_coord, y_coord]

                if(char == '\n'):
                    continue
                line_element.append(char)

                y_coord +=1 
            
            print(line_element)
            output.append(line_element)

            x_coord += 1

    return output, start, end
        
if __name__ == '__main__':
    get_resources()
    # print("1 1 ",board[0][0] )