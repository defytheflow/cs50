# Checks whether credit card number is valid using Luhn's algorithm.


def main():
    card_number = get_card_number()
    card_type = get_card_type(card_number)
    if card_type == "INVALID":
        print(card_type)
    else:
        check_luhn(card_number, card_type)


def get_card_number() -> str:
    """ Prompts user for valid credit card number. """
    while True:
        card_number = input("Number: ")
        if card_number.isdigit():
            break
    return card_number


def get_card_type(card: str) -> str:
    """ Returns the type of the card based on its length. """
    if card[0] == "4" and (len(card) == 13 or len(card) == 16):
        return "VISA"
    elif (card[:2] in ("34", "37")) and len(card) == 15:
        return "AMEX"
    elif len(card) == 16 and card[:2] in ("51", "52", "53", "54", "55"):
        return "MASTERCARD"
    else:
        return "INVALID"


def check_luhn(card, card_type):
    """ Checks if the card number is valid using Luhn's algorithm. """
    sum1 = 0
    sum2 = 0
    if len(card) % 2 != 0:
        for ind, num in enumerate(card):
            if ind % 2 == 0:
                sum2 += int(card[ind])
            else:
                num = int(card[ind]) * 2
                if num > 9:
                    sum1 += num // 10 + num % 10
                else:
                    sum2 += num
        if (sum1 + sum2) % 10 == 0:
            print(card_type)
        else:
            print("INVALID")
    else:
        for ind, num in enumerate(card):
            if ind % 2 != 0:
                sum2 += int(card[ind])
            else:
                num = int(card[ind]) * 2
                if num > 9:
                    sum1 += num // 10 + num % 10
                else:
                    sum2 += num
        if (sum1 + sum2) % 10 == 0:
            print(card_type)
        else:
            print("INVALID")


if __name__ == "__main__":
    main()