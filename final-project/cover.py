import sys
import random
import argparse

from PIL import Image
from bitarray import bitarray

from helpers import show_execution_time
from helpers import (get_image, check_image_format, check_image_mode,
                     check_image_width)
from helpers import P_PIXEL, RGB_PIXEL, RGBA_PIXEL


@show_execution_time
def main():
    args = parse_args()
    img = get_image(args.image)
    message = binary(args.message)
    check_image_format(img)
    check_image_mode(img)
    copy_img = copy_image(img)
    covered_img = cover(copy_img, message)
    if args.output:
        covered_img.save(args.output)
    else:
        covered_img.save(f"hidden.{img.format.lower()}")


def cover(img: Image, message: bitarray) -> Image:
    """ Returns the input Image with covered message inside of it. """
    width, height = img.size
    check_image_width(width, RGB_PIXEL, message)
    pixels = img.load()

    row = random.randint(0, height)  # Randomly chooses row.
    i = 0  # Tracks hidden bits

    # If Image consist of 8-bit pixels
    if img.mode == "P":
        offset = generate_offset(width, P_PIXEL, message)
        for x in range(offset, width):
            p = pixels[x,row]
            if i < len(message):
                p = modify_byte(p, message[i])
                i += 1
            pixels[x,row] = p
        generate_key(row, message, offset * P_PIXEL)
    # If Image consists of 3x8-bit pixels
    elif img.mode == "RGB":
        offset = generate_offset(width, RGB_PIXEL, message)
        for x in range(offset, width):
            r, g, b = pixels[x,row]
            if i < len(message):
                r = modify_byte(r, message[i])
                i += 1
            if i < len(message):
                g = modify_byte(g, message[i])
                i += 1
            if i < len(message):
                b = modify_byte(b, message[i])
                i += 1
            pixels[x,row] = (r, g, b)
        generate_key(row, message, offset * RGB_PIXEL)
    # If Image consists of 4x8-bits pixels
    elif img.mode == "RGBA":
        offset = generate_offset(width, RGBA_PIXEL, message)
        for x in range(offset, width):
            r, g, b, a = pixels[x,row]
            if i < len(message):
                r = modify_byte(r, message[i])
                i += 1
            if i < len(message):
                g = modify_byte(g, message[i])
                i += 1
            if i < len(message):
                b = modify_byte(b, message[i])
                i += 1
            if i < len(message):
                a = modify_byte(a, message[i])
                i += 1
            pixels[x,row] = (r, g, b, a)
        generate_key(row, message, offset * RGBA_PIXEL)

    return img


def copy_image(img: Image) -> Image:
    """ Returns the exact copy of a given Image. """
    width, height = img.size
    new_img = Image.new(img.mode, img.size)
    new_pixels = new_img.load()  # New Image pixels, default: all black.
    pixels = img.load()  # Input Image pixels.
    for x in range(width):
        for y in range(height):
            new_pixels[x,y] = pixels[x,y]
    return new_img


def modify_byte(byte: int, message_bit: bool) -> int:
    """ Returns byte with modified Least Significant Bit. """
    byte = bin(byte)
    byte_new_last_bit = int(message_bit)
    new_byte = int(byte[:-1] + str(byte_new_last_bit), base=2)
    return new_byte


def generate_key(row: int, message: bitarray, offset: int):
    """
    Generates key for the uncovering process.
    R - stands for row, so digits after R represent the row.
    L - stands for length, so digits after L represent the length
        of the message in bits.
    O - offset from the beggining of the row.
    """
    row = "R" + str(row)
    length = "L" + str(len(message))
    offset = "O" + str(offset)
    key = []
    key.extend([row, length, offset])
    random.shuffle(key)
    print(f"Key: {''.join(key)}")


def generate_offset(width: int, bytes_in_pixel: int, message: bitarray) -> int:
    """ Returns a random offset. """
    possible_offset = width * bytes_in_pixel - len(message)
    offset = random.randint(0, possible_offset)
    return offset // bytes_in_pixel


def binary(message: str) -> bitarray:
    """
    Returns it's input binary representation.

    >>> binary("a")
    bitarray('01100001')
    >>> binary("1")
    bitarray('00110001')

    """
    binary_message = bitarray()
    byte_message = bytes(message, encoding="ascii")
    binary_message.frombytes(byte_message)
    return binary_message


def parse_args() -> argparse.Namespace:
    """ Returns specified command line arguments. """
    parser = argparse.ArgumentParser(prog="cover.py",
    description="Covers your message in a given image, using LSB Stegonography technique.")
    #  Positional arguments
    parser.add_argument("image", help="Image in which to cover your secret message.")
    parser.add_argument("message", help="Message to cover in your image.")
    # Optional arguments
    parser.add_argument("-o", "--output",
    help="Name of the output image with hidden message in it.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
    sys.exit(0)
