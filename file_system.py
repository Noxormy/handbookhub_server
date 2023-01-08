import os
import base64
import yaml


ENCODING = 'utf-8'


def get_base64_image(path) -> str:
    if not os.path.exists(path) or os.path.isdir(path):
        return ''

    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode(ENCODING)


def get_text_file(path) -> str:
    if not os.path.exists(path) or os.path.isdir(path):
        return ''

    with open(path, 'rb') as file:
        return file.read().decode(ENCODING)


def get_yaml_file(path) -> str:
    if not os.path.exists(path) or os.path.isdir(path):
        return ''

    with open(path, 'rb') as file:
        return yaml.safe_load(file)
