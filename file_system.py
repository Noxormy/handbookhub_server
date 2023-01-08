"""
    This module provide functions which help get data from disk
"""

import os
import base64
import yaml

from logger import logger

ENCODING = "utf-8"


def get_base64_image(path: str) -> str:
    """
    Returns the base64 encoded string of image at the following path
    Or empty string if there is no file
            Parameters:
                    path: str - A path to an image
            Returns:
                    str - Base64 encoded string
    """
    if not os.path.exists(path) or os.path.isdir(path):
        logger.error(f"Can't find image on path {path}")
        return ""

    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode(ENCODING)


def get_text_file(path: str) -> str:
    """
    Returns the string of the file at the following path
    Or empty string if there is no file
            Parameters:
                    path: str - A path to a text file
            Returns:
                    str - file content
    """
    if not os.path.exists(path) or os.path.isdir(path):
        logger.error(f"Can't find text file on path {path}")
        return ""

    with open(path, "rb") as file:
        return file.read().decode(ENCODING)


def get_yaml_file(path) -> dict:
    """
    Returns the dict with the parsed yaml file at the following path
    Or empty dict if there is no file
            Parameters:
                    path: str - A path to a text file
            Returns:
                    str - file content
    """
    if not os.path.exists(path) or os.path.isdir(path):
        logger.error(f"Can't find yaml file on path {path}")
        return {}

    with open(path, "rb") as file:
        return yaml.safe_load(file)
