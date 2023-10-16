# import random
# import sympy

# region

# def KR(text, pattern):

#     tl = len(text)              # text length
#     pl = len(pattern)           # pattern length

#     prime_limit = 1000
#     p = sympy.randprime(2, prime_limit)
#     # p = 101

#     results = []


#     # Hash value for pattern #
#     hash_pattern = 0
#     d = 256                     # ASCII alphabet size
#     for i in range(pl):         # przechodzimy po wszystkich znakach wzorca

#         hash_pattern += ord(pattern[i]) * pow(d, pl-i-1, p)     # wartość hasza dla każdego znaku dodajemy do sumy
#                                                                 # otrzymujemy unikalny hasz dla danego znaku w pattern, który uwzględnia zarówno wartość znaku, jak i jego pozycję wewnątrz wzorca
#         hash_pattern %= p                                       # reszta z dzielenia sumy przez p


#     # Hash value for consecutive "windows"
#     window_hash = 0
#     h = 1
#     for i in range(pl-1):                                       # obliczamy wartość h dla każdego kolejnego okna
#         h = (h * d) % p

#     for i in range(pl):                                         # przechodzimy po wszystkich znakach pierwszego okna
#         window_hash = (d * window_hash + ord(text[i])) % p


#     # Comparing window hash with text hash, char by char
#     for i in range(tl - pl + 1):

#         if hash_pattern == window_hash:

#             if pattern == text[i:i+pl]:                         # dodatkowe sprawdzenie czy wzorzec jest w tekście (gdyby hasz się powtórzył)
#                 results.append(i+1)

#                                                                 # obliczamy wartość hasza dla kolejnego okna tekstu, przesuwając okno o jeden znak
#         if i < tl - pl:                                         # wartość hasza musi być nieujemna
#             window_hash = (d * (window_hash - ord(text[i]) * h) + ord(text[i+pl])) % p
#             window_hash = (window_hash + p) % p

#     return results

# endregion


def KR_search(pattern, text):

    tl = len(text)
    pl = len(pattern)
    results = []

    if (pl > tl or pl == 0 or tl == 0):
        return results

    # suma wartości ASCII poszzcególnych znaków wzorca
    hash_pattern = sum(ord(pattern[i]) for i in range(pl))

    window_hash = sum(ord(text[i]) for i in range(pl))

    # iteracja po wszystkich możliwych pozycjach początkowych "okienek" tekstu, które są dostatecznie długie, aby pomieścić cały wzorzec
    for i in range(tl - pl + 1):

        # porównanie hasza wzorca w haszem bieżącego okienka
        # oraz sam wzorzec z podciągiem tekstu
        if hash_pattern == window_hash and pattern == text[i:i+pl]:
            results.append(i)

        # sprawdzenie czy nie jesteśmy na ostatnim okienku tekstu
        # ponieważ dla każdej iteracji pętli przesuwamy "okienko" o jeden znak w prawo, musimy upewnić się, że nie wykraczamy poza granice tekstu
        # jeśli warunek jest spełniony, następuje aktualizacja wartości hasza "okienka"
        if i < tl - pl:
            window_hash = window_hash - ord(text[i]) + ord(text[i+pl])

    return results


def main():

    text = "FEANNBGRANNBCD"
    pattern = "NNB"

    result = KR2(text, pattern)

    if len(result) == 0:
        print("Pattern not found")

    else:
        print("Pattern found on postion: " + str(result))


if __name__ == '__main__':
    main()
