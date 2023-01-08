import os

ENCODING = 'utf-8'


def is_dir_existed(path) -> bool:
    return os.path.isdir(path)


def get_text_file(path) -> str:
    with open(path, 'rb') as text_file:
        return text_file.read().decode(ENCODING)
