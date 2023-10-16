
def KMP_search(pattern, text):
    pattern_size = len(pattern)
    text_size = len(text)

    positions_list = []

    if (pattern_size > text_size or text_size == 0 or pattern_size == 0):
        return positions_list

    LPS = create_LPS_array(pattern)

    pattern_index = 0
    text_index = 0

    while (text_size - text_index) >= (pattern_size - pattern_index):
        if (pattern[pattern_index] == text[text_index]):
            pattern_index += 1
            text_index += 1

        if pattern_index == pattern_size:
            positions_list.append(text_index-pattern_index)
            pattern_index = LPS[pattern_index-1]

        elif text_index < text_size and pattern[pattern_index] != text[text_index]:
            if pattern_index != 0:
                pattern_index = LPS[pattern_index-1]
            else:
                text_index += 1
    return positions_list


def create_LPS_array(pattern):
    pattern_size = len(pattern)

    LPS = [0] * pattern_size
    # length of longest prefix-suffix
    length = 0

    index = 1

    while index < pattern_size:

        if pattern[index] == pattern[length]:
            length += 1
            LPS[index] = length
            index += 1

        else:
            if length != 0:
                length = LPS[length-1]

            else:
                LPS[index] = 0
                index += 1

    return LPS


if __name__ == '__main__':
    txt = "AABAACAADAABAABAA"
    pat = "AABA"

    print(KMP_search(pat, txt))
