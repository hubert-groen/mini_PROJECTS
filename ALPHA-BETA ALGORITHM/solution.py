from two_player_games.games.morris import SixMensMorris
import random
import copy
import matplotlib.pyplot as plt
import time

def heurystyka(board):          # zwraca różnicę pionków gracza 1 i 2, dla obecnego statu planszy (grid)
    pawn_1 = 0
    pawn_2 = 0
    for n in board:
        if hasattr(n, 'char'):
            if n.char == '1':
                pawn_1 += 1
            elif n.char == '2':
                pawn_2 += 1
    pawns_difference = abs(pawn_1 - pawn_2)
    return pawns_difference


def minimax_alphabeta(game, depth, alpha, beta, maximizing_player):

    if depth == 0 or game.is_finished():
        return heurystyka(game.state.grid)
    
    if maximizing_player:
        max_val = float('-inf')
        for move in game.get_moves():
            game_temp = copy.deepcopy(game)         # deepcopy() tworzy nowy, niezależny obiekt gry; lepsze rozwiązanie niż "game_temp = game"
            game_temp.make_move(move)
            val = minimax_alphabeta(game_temp, depth-1, alpha, beta, False)     # oceniamy wartość dla każdego z dostępnych ruchów (False - "z perspektywy" przeciwnika)
            
            max_val = max(max_val, val)             # obcinanie alfa-beta oszczędza dużo czasu
            alpha = max(alpha, max_val)             # nie zagłębiamy się w ruchy, których przeciwnik i tak nie wykona (ponieważ są dla niego nieoptymalne)
            if alpha >= beta:
                break

        return max_val
    
    else:                                           # analogicznie dla gracza minimalizującego
        min_val = float('inf')
        for move in game.get_moves():
            game_temp = copy.deepcopy(game)
            game_temp.make_move(move)
            val = minimax_alphabeta(game_temp, depth-1, alpha, beta, True)

            min_val = min(min_val, val)
            beta = min(beta, min_val)
            if beta <= alpha:
                break

        return min_val


def solve(num_games, d1, d2):

    game_results = []                                           # tutaj będą przechowywane końcowe rezultaty dla wielu uruchomień gry

    for game_num in range(num_games):
        game = SixMensMorris()
        round_counter = 0

        while not game.is_finished():
            round_counter += 1

            current_player = game.get_current_player()          # sprawdzamy kto wykonuje ruch dla obecnego stanu gry
            if current_player == 1:                             # i uruchamiamy minimax z jego głębokością
                depth = d1                                      # głębokość drugiego gracza nie jest potrzebna w tym kroku
            else:
                depth = d2

            current_moves = game.get_moves()                    # pobieramy wszystkie możliwe ruchy
            random.shuffle(current_moves)                       # i oceniamy ich wartość w kolejności losowej
            best_move = None                                    # to uniknie powtarzalności tych samych wariantów
            best_val = float('-inf')

            for move in current_moves:
                if current_player == 1:
                    move_val = minimax_alphabeta(game, depth-1, float('-inf'), float('inf'), True)          # maksymalizujemy wartość oceny
                else:
                    move_val = minimax_alphabeta(game, depth-1, float('-inf'), float('inf'), False)         # minimalizujemy wartość oceny

                if move_val > best_val:
                    best_val = move_val
                    best_move = move                            
                                                                # nie musimy kolejny raz losować ruchu z najlepszych możliwych, ponieważ i tak losowanie było wcześniej
            game.make_move(best_move)                           # wykonamy ruch z najlepszą dotychczas wartością oceny

        winner = game.get_winner()                              # sprawdzenie wyniku
        if winner is None:
            winner = 0
        elif winner.char == '1':
            winner = 1
        else:
            winner = 2

        game_results.append(winner)                             # wrzucenie na stos do statystyk
        print("Game " + str(game_num+1) + " - Winner: " + str(winner))

    return game_results


def plot_results(results, n, d1, d2):        # liczy zwycięzców/remisy w tablicy rezultatów
    labels = ['Player 1', 'Player 2', 'Draw']
    values = [results.count(1), results.count(2), results.count(0)]
    colors = ['#99ff99','#ff9999','#cccccc']

    plt.pie(values, labels=labels, colors=colors, autopct='%d%%', startangle=90)
    plt.axis('equal')

    plt.title('SixMensMorris with MIMINAX', y=1.05)

    plt.text(1.7, -1.2, f"# of runs:            {n}\ndepth player 1:       {d1}\ndepth player 2:       {d2}", ha='right', va='bottom', fontsize=10)

    plt.show()


if __name__ == '__main__':

    # PARAMETRY WEJŚCIOWE
    number_of_games = 5
    depth_player_1 = 2
    depth_player_2 = 1

    # URUCHOMIENIE ALGORYTMU
    start_time = time.time()
    results = solve(number_of_games, depth_player_1, depth_player_2)
    end_time = time.time()

    # CZAS
    elapsed_time = end_time- start_time
    elapsed_time = round(elapsed_time, 2)

    # WYKRES
    plot_results(results, number_of_games, depth_player_1, depth_player_2)