import re
import sys
import argparse

from PIL import Image

from helpers import show_execution_time
from helpers import get_image, check_image_format, check_image_mode, chararray
from helpers import P_PIXEL, RGB_PIXEL, RGBA_PIXEL


@show_execution_time
def main():
    args = parse_args()
    img = get_image(args.image)
    check_image_format(img)
    check_image_mode(img)
    message = discover(img, args.key)
    print("Message:", message)


def discover(img: Image, key: str) -> str:
    """ Discovers the hidden message using special key from the Image. """
    found_bits = ""
    width, _ = img.size
    pixels = img.load()

    row, message_length, offset = parse_key(key)
    i = 0  # Tracks found bits

    # If Image consist of 8-bit pixels
    if img.mode == "P":
        for x in range(offset // P_PIXEL, width):
            p = pixels[x,row]
            if i < message_length:
                found_bits += bin(p)[-1]
                i += 1
    # If Image consists of 3x8-bit pixels
    elif img.mode == "RGB":
        for x in range(offset // RGB_PIXEL, width):
            r, g, b = pixels[x,row]
            if i < message_length:
                found_bits += bin(r)[-1]
                i += 1
            if i < message_length:
                found_bits += bin(g)[-1]
                i += 1
            if i < message_length:
                found_bits += bin(b)[-1]
                i += 1
    # If Image consists of 4x8-bits pixels
    elif img.mode == "RGBA":
        for x in range(offset // RGBA_PIXEL, width):
            r, g, b, a = pixels[x,row]
            if i < message_length:
                found_bits += bin(r)[-1]
                i += 1
            if i < message_length:
                found_bits += bin(g)[-1]
                i += 1
            if i < message_length:
                found_bits += bin(b)[-1]
                i += 1
            if i < message_length:
                found_bits += bin(a)[-1]
                i += 1
    chars = chararray(found_bits)
    return "".join(chars)


def parse_key(key: str) -> tuple:
    """ Returns row, length and offset of the covered message,
        parsed from the key. """
    res = re.findall("R[0-9]*|L[0-9]*|O[0-9]*", key)
    for s in res:
        if s.startswith("R"):
            row = int(s[1:])
        elif s.startswith("L"):
            length = int(s[1:])
        elif s.startswith("O"):
            offset = int(s[1:])
    return row, length, offset


def parse_args() -> argparse.Namespace:
    """ Returns specified command line arguments. """
    parser = argparse.ArgumentParser(prog="discover.py",
    description="Discovers your message from a given image, using LSB Stegonography technique.")
    #  Positional arguments
    parser.add_argument("image", help="Image in which your secret message is covered.")
    parser.add_argument("key", help="A key given to you when you were covering your message.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
    sys.exit(0)
