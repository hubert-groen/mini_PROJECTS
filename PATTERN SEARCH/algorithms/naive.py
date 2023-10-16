
def naive_search(pattern, text):
    text_size = len(text)
    pattern_size = len(pattern)
    positions_list = []
    if (pattern_size > text_size or text_size == 0 or pattern_size == 0):
        return positions_list

    for index in range(text_size - pattern_size + 1):

        pattern_index = 0

        while (pattern_index < pattern_size):
            if (text[index+pattern_index] != pattern[pattern_index]):
                break
            pattern_index += 1

        if (pattern_index == pattern_size):
            positions_list.append(index)

    return positions_list


if __name__ == '__main__':
    txt = "AABAACAADAABAABAA"
    pat = "AABA"

    print(naive_search(pat, txt))
