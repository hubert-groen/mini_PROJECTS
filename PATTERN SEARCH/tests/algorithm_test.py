from algorithms.naive import naive_search
from algorithms.KR_2 import KR_search
from algorithms.KMP import KMP_search

ALGORITHMS =\
    {
        'KMP': KMP_search,
        'KR': KR_search,
        'naive': naive_search,
    }

TEST_PATTERN = 'AB'
TEST_TEXT = 'ABABA'


def test_empty():
    for _, algorithm in ALGORITHMS.items():
        assert (algorithm('', '') == [])
        assert (algorithm(TEST_PATTERN, '') == [])
        assert (algorithm('', TEST_TEXT) == [])


def test_same_pattern_as_text():
    for _, algorithm in ALGORITHMS.items():
        assert (algorithm(TEST_PATTERN, TEST_PATTERN) == [0])
        assert (algorithm(TEST_PATTERN, TEST_PATTERN) == [0])
        assert (algorithm(TEST_PATTERN, TEST_PATTERN) == [0])


def test_pattern_longer_than_text():
    for _, algorithm in ALGORITHMS.items():
        assert (algorithm(TEST_TEXT, TEST_PATTERN) == [])
        assert (algorithm(TEST_TEXT, TEST_PATTERN) == [])
        assert (algorithm(TEST_TEXT, TEST_PATTERN) == [])


def test_pattern_not_in_text():
    for _, algorithm in ALGORITHMS.items():
        assert (algorithm('C', TEST_TEXT) == [])
        assert (algorithm('C', TEST_TEXT) == [])
        assert (algorithm('C', TEST_TEXT) == [])
