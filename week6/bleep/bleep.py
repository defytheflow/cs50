# Bleeps words with * sign if they are in banned.txt
import sys


def main():
    check_args()
    filename = sys.argv[1]
    banned_words = get_banned_words(filename)
    message = input("What message would you like to censor?\n")
    censor(message, banned_words)


def check_args() -> bool:
    """ Checks provided command line arguments. """
    if len(sys.argv) != 2:
        print("Usage bleep.py dictionary")
        sys.exit(1)


def get_banned_words(file: str) -> set:
    """ Retrieves banned words from the given file. """
    banned_words = set()
    with open(file) as f:
        for word in f:
            banned_words.add(word.rstrip())
    return banned_words


def censor(message: str, banned_words: set):
    """ Checks if message contains banned words, and replaces them with *."""
    censored_message = []
    for mes in message.split():
        if mes.lower() in banned_words:
            censored_message.append("*" * len(mes))
        else:
            censored_message.append(mes)
    print(" ".join(censored_message))


if __name__ == "__main__":
    main()
