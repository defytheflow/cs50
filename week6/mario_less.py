# Prompts user for the height and prints out pyramid from mario


def main():
    height = get_height()
    draw_pyramid(height)


def get_height():
    """ Prompts user for height of the pyramid. """
    while True:
        height = input("Height: ")
        if height.isdigit():
            height = int(height)
            if (1 <= height <= 8):
                break
    return height


def draw_pyramid(height: int):
    """ Draws pyramid to the console. """
    block = "#"
    space = " "
    for i in range(1, height+1):
        print(space*(height-i), block*i, sep="")


if __name__ == "__main__":
    main()