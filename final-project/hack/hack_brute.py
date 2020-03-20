# This script is under development.

import sys
import argparse

from PIL import Image

from helpers import get_image, check_image_format, check_image_mode, chararray
from helpers import P_PIXEL, RGB_PIXEL, RGBA_PIXEL


def main():
    args = parse_args()
    img = get_image(args.image)
    check_image_format(img)
    check_image_mode(img)
    message = discover(img)
    print(message)
    sys.exit(0)


def discover(img: Image) -> str:
    """ Attempts to discover hidden message in the Image. """
    lsbits = ""  # least significant bits
    width, height = img.size
    pixels = img.load()

    y = 268
    print(img.mode)
    print(width)
    print(height)

    if img.mode == "P":
        for x in range(width):
            p = pixels[x,y]
            lsbits += bin(p)[-1]
    elif img.mode == "RGB":
        for x in range(1, width):
            r, g, b = pixels[x,y]
            lsbits += bin(r)[-1]
            lsbits += bin(g)[-1]
            lsbits += bin(b)[-1]
    elif img.mode == "RGBA":
        for x in range(1, width):
            for y in range(height):
                r, g, b, a = pixels[x,y]
                lsbits += bin(r)[-1]
                lsbits += bin(g)[-1]
                lsbits += bin(b)[-1]
                lsbits += bin(a)[-1]
    chars = chararray(lsbits)
    print(len(chars))
    return chars


def parse_args() -> argparse.Namespace:
    """ Returns command line arguments. """
    parser = argparse.ArgumentParser(prog="discover.py",
    description="Tests vulnerabilities in the result of cover.py script.")
    #  Positional arguments
    parser.add_argument("image", help="Image in which secret message is covered.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
