# Encrypts given message using Vigenere Cipher
import sys


def main():
    check_args()
    keyword = sys.argv[1]
    message = input("plaintext: ")
    encrypt_vigenere(message, keyword)


def check_args() -> bool:
    """ Checks provided command line arguments. """
    if len(sys.argv) == 2:
        keyword = sys.argv[1]
        for ch in keyword:
            if ch.isdigit():
                print("Usage viginere.py keyword")
                sys.exit(1)
    else:
        print("Usage vigenere.py keyword")
        sys.exit(1)


def encrypt_vigenere(message: str, keyword: str) -> None:
    """ Encrypts the message using Vigenere Cipher. """
    encr_message = ""
    key = 0
    for ch in message:
        if ch.isalpha():
            if key == len(keyword):
                key = 0
            encr_message += encrypt_caesar(ch, shift(keyword[key]))
            key += 1
        else:
            encr_message += ch
    print("ciphertext:", encr_message)


def shift(ch: str):
    """ Returns key for Caesar Encryption. """
    return ord(ch.lower()) - ord("a")


def encrypt_caesar(ch: str, k: int) -> str:
    """ Returns message encrypted using Caesar Cipher. """
    if 64 < ord(ch) and ord(ch) < 91:
        if 64 < ord(ch) + k and ord(ch) + k < 91:
            return chr(ord(ch) + k)
        else:
            return chr(ord(ch) + k - 26)
    elif 96 < ord(ch) and ord(ch) < 123:
        if 96 < ord(ch) + k and ord(ch) + k < 123:
            return chr(ord(ch) + k)
        else:
            return chr(ord(ch) + k - 26)


if __name__ == "__main__":
    main()