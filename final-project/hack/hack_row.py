import sys
import string
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
    discover(img, args.row)


def last_bits_to_ascii(bytes: list) -> str:
    """ Translates last bits of integers in binary into a char. """
    if len(bytes) != 8:
        raise ValueError("Bytes list must be have length 8.")
    char = [i[-1] for i in bytes]
    char = "".join(char)
    char = chr(int(char, base=2))
    return char


def pixels_to_binary(img: Image, row: int) -> list:
    """
        Translates all inregers representing pixels into binary
        and return it as array.
    """
    width, _ = img.size
    pixels = img.load()
    bin_array = []
    for x in range(width):
        p = pixels[x,row]
        bin_array.append(bin(p))
    return bin_array


def discover(img: Image, row: int) -> str:
    """ Attempts to discover hidden message in the Image. """
    width, _ = img.size
    letters = []
    BYTE = 8
    if img.mode == "P":
        bin_array = pixels_to_binary(img, row)
        i = 0
        while i < width:
            char = []
            for j in range(BYTE):
                try:
                    char.append(bin_array[i+j])
                except IndexError:
                    break
            try:
                char = last_bits_to_ascii(char)
            except ValueError:
                break
            else:
                if char in string.ascii_letters or char in " ":
                    letters.append(char)
                    i += 8
                else:
                    i += 1

        print("".join(letters))


def parse_args() -> argparse.Namespace:
    """ Returns command line arguments. """
    parser = argparse.ArgumentParser(prog="hack.py",
    description="Tests vulnerabilities in the result of cover.py script.")
    #  Positional arguments
    parser.add_argument("image", help="Image in which secret message is covered.")
    parser.add_argument("row", type=int, help="Row in which message is hidden.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
    sys.exit(0)
