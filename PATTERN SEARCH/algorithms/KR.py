import sympy


def KR_search(pattern, text):

    tl = len(text)              # text length
    pl = len(pattern)           # pattern length
    results = []

    if (pl > tl or pl == 0 or tl == 0):
        return results

    # prime_limit = 1000
    # p = sympy.randprime(2, prime_limit)
    p = 13399

    # Hash value for pattern #
    hash_pattern = 0
    d = 256                     # ASCII alphabet size
    for i in range(pl):         # przechodzimy po wszystkich znakach wzorca

        # wartość hasza dla każdego znaku dodajemy do sumy
        hash_pattern += ord(pattern[i]) * pow(d, pl-i-1)
        # reszta z dzielenia sumy przez p
    hash_pattern %= p

    # Hash value for consecutive "windows"
    window_hash = 0
    h = 1
    # obliczamy wartość h dla każdego kolejnego okna
    for i in range(pl-1):
        h = (h * d) % p

    # przechodzimy po wszystkich znakach pierwszego okna
    for i in range(pl):
        window_hash = (d * window_hash + ord(text[i])) % p

    # Comparing window hash with text hash, char by char
    for i in range(tl - pl + 1):

        if hash_pattern == window_hash:

            # dodatkowe sprawdzenie czy wzorzec jest w tekście (gdyby hasz się powtórzył)
            if pattern == text[i:i+pl]:
                # wzorzec znaleziony
                results.append(i)

                # obliczamy wartość hasza dla kolejnego okna tekstu, przesuwając okno o jeden znak
        if i < tl - pl:                                         # wartość hasza musi być nieujemna
            window_hash = (
                d * (window_hash - ord(text[i]) * h) + ord(text[i+pl])) % p
            # window_hash = (window_hash + p) % p

    return results


def main():

    text = "FEANNBGRANNBCD"
    pattern = "BCD"

    result = KR_search(pattern, text)

    if len(result) == 0:
        print("Pattern not found")

    else:
        print("Pattern found on postion: " + str(result))


if __name__ == '__main__':
    main()
