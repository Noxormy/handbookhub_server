import base64

ENCODING = 'utf-8'


def get_base64_image(path) -> str:
    with open(path, 'rb') as image_file:
        return  base64.b64encode(image_file.read()).decode(ENCODING)
