import os
import platform

DIRNAME = os.path.dirname(__file__)

if (platform.system() == 'Windows'):
    PAN_TADEUSZ_DIR = os.path.join(DIRNAME, 'pan-tadeusz-windows.txt')
else:
    PAN_TADEUSZ_DIR = os.path.join(DIRNAME, 'pan-tadeusz-unix.txt')


def get_resources():
    """function reading txt file and returning array of words"""
    with open(PAN_TADEUSZ_DIR, 'r', encoding='utf-8') as file:
        return file.read().split()


if __name__ == '__main__':
    get_resources()
