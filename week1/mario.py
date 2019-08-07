def main():
    height = prompt()
    draw(height)

def prompt():
    while True:
        try:
            height = int(input("Give me an integer from 0 through 8: "))
        except ValueError as e:
            print(e)
            continue
        
        if not (0 < height < 9):
            continue
 
        return height


def draw(height: int):
    hash = "#"
    spaces = height-1
    for i in range(1, height+1): 
        print(spaces*" " + hash*i + "  " + hash*i + spaces*" ")
        spaces -= 1


if __name__ == "__main__":
    main()




