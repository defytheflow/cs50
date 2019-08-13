# Draws a pyramid from mario game after prompting user for height


def main():
    height = get_height()
    draw_pyramid(height)


def get_height():
    """ Prompts user for height of the pyramid. """
    while True:
        height = input("Height: ")
        if height.isdigit():
            height = int(height)
            if 1 <= height <= 8:
                break
    return height


def draw_pyramid(height: int):
    """ Draws pyramid to the console. """
    block = "#"
    spaces = height-1
    for i in range(1, height+1):
        print(spaces*" " + block*i + "  " + block*i)
        spaces -= 1


if __name__ == "__main__":
    main()
