# Calculates the minimum amount of coins for a particular sum of cash


def main():
    cash = get_cash()
    calc_coins(cash)


def get_cash():
    """ Prompts user for cash in dollars. """
    while True:
        cash = input("Change owed: ")
        try:
            cash = float(cash)
        except ValueError:
            continue
        else:
            if 0 <= cash:
                return cash


def calc_coins(cash: float):
    """ Calculates the minimum amount of coint for the cash. """
    cents = round(cash*100)
    coins = 0
    if cents >= 25:
        quarters = cents // 25
        cents -= quarters * 25
        coins += quarters
    if cents >= 10:
        dimes = cents // 10
        cents -= dimes * 10
        coins += dimes
    if cents >= 5:
        nickels = cents // 5
        cents -= nickels * 5
        coins += nickels
    if cents > 0:
        pennies = cents // 1
        coins += pennies
    print(coins)


if __name__ == "__main__":
    main()
