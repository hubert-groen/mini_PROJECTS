import heapq
from resources.get_resources import get_resources


def dijkstra(matrix, start, end):

    rows = len(matrix)
    cols = len(matrix[0])

    distances = [[float('inf')] * cols for _ in range(rows)]        # początkowo wszystkie koszty na infinity
    distances[start[0]][start[1]] = 0                               # odległość od startowego węzła do samego siebie wynosi 0
    previous = [[None] * cols for _ in range(rows)]                 # inicjalizacja tablicy poprzedników

    heap = [(0, start)]                                             # kopiec priorytetowy, który będzie przechowywał węzły do odwiedzenia

    while heap:                                                     # dopóki coś jest w kopcu

        current_distance, current_node = heapq.heappop(heap)        # ??? pobranie węzła o najmniejszej odległości

        if current_node == end:
            return distances[end[0]][end[1]], previous

        for neighbor in get_neighbors(matrix, current_node):
            row, col = neighbor
            cost = int(matrix[row][col])                                    # koszt sąsiada

            if current_distance + cost < distances[row][col]:               # RELAKSACJA (aktualizacja kosztu przejścia do węzła, jeśli znaleziono mniejszy)
                distances[row][col] = current_distance + cost
                previous[row][col] = current_node
                heapq.heappush(heap, (distances[row][col], (row, col)))     # dodanie sąsiada do kolejki priorytetowej

    return -1, []


def get_neighbors(matrix, node):

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []

    for direction in directions:
        row = node[0] + direction[0]
        col = node[1] + direction[1]

        if is_valid(matrix, row, col):                                  # jeśli sąsiad "jest ważny", dodajemy go do listy sąsiadów
            neighbors.append((row, col))

    return neighbors


def is_valid(matrix, row, col):

    rows = len(matrix)
    cols = len(matrix[0])

    # sprawdzenie, czy wiersz i kolumna są w granicach macierzy oraz czy pole nie jest puste
    return 0 <= row < rows and 0 <= col < cols and matrix[row][col] != ' '


def find_shortest_path(filename = 'example_2.txt'):
    board, s, e = get_resources()

    start_point = (s[0], s[1])
    end_point = (e[0], e[1])

    board[s[0]][s[1]] = 0
    board[e[0]][e[1]] = 0


    shortest_path_cost, previous_nodes = dijkstra(board, start_point, end_point)

    if shortest_path_cost != -1:

        print("Najmniejszy koszt ścieżki:", shortest_path_cost)

        path = []
        current_node = end_point

        while current_node != start_point:

            path.append(current_node)
            current_node = previous_nodes[current_node[0]][current_node[1]]

        path.append(start_point)
        path.reverse()

        print("Ścieżka:", path)

    else:
        print("Nie znaleziono ścieżki")


    for i in range(len(board)):
        for j in range(len(board[i])):
            if (i, j) not in path:
                board[i][j] = ' '

            if (board[i][j] == 0):
                board[i][j] = 'X'

    for row in board:
        print(row)


if __name__ == '__main__':
    find_shortest_path()
