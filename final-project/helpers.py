import sys

from PIL import Image
from bitarray import bitarray


SUPPORTED_FORMATS = ("PNG", )
SUPPORTED_MODES = ("P", "RGB", "RGBA")

# Size in bytes of each pixel
P_PIXEL = 1
RGB_PIXEL = 3
RGBA_PIXEL = 4


def show_execution_time(func):
    """ This decorator prints out Execution time of the input function. """
    import time

    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print("Execution time:", end - start)
    return wrapper


def get_image(img_name: str) -> Image:
    """ Returns Image object, prior checking if image exists. """
    try:
        img = Image.open(img_name)
    except IOError:
        print(f"Could not open image {img_name}.")
        sys.exit(1)
    else:
        return img


def check_image_format(img: Image):
    """ Checks if Image format is supported. """
    if img.format not in SUPPORTED_FORMATS:
        print(f"This image format is {img.format}. It is not supported.")
        sys.exit(1)


def check_image_mode(img: Image):
    """ Checks if Image mode is supported. """
    if img.mode not in SUPPORTED_MODES:
        print(f"This image mode is {img.mode}. It is not supported.")
        sys.exit(1)


def check_image_width(width: int, bytes_in_pixel: int, message: bitarray):
    """ Checks if Image's first row has enough space to hide the message. """
    if width * bytes_in_pixel < len(message):
        print(f"This image is not wide enough for that key.")
        sys.exit(1)


def chararray(bits: str) -> list:
    """
    Returns list of characters from it's binary representation.

    >>> chararray("01000001")
    ['A']
    >>> chararray("01100001")
    ['a']

     """
    BYTE = 8  # BYTE is 8 bits
    chars = []
    for i in range(0, len(bits), BYTE):
        char = bits[i:i+BYTE]
        chars.append(char)
    chars = [chr(int(ch, base=2)) for ch in chars]
    return chars
