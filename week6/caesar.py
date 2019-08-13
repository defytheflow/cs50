# This program encrypts the given message by a given key using Caesar Cipher
import sys


def main():
    check_args()
    key = int(sys.argv[1]) % 26
    message = input("plaintext: ")
    encrypt_caesar(message, key)


def check_args() -> bool:
    """ Checks provided command lines arguments. """
    if len(sys.argv) == 2:
        key = sys.argv[1]
        if not key.isdigit():
            print("Usage caesar.py k")
            sys.exit(1)
    else:
        print("Usage caesar.py k")
        sys.exit(1)


def encrypt_caesar(message: str, k: int) -> None:
    """ Encrypts te message using Caesar Cipher. """
    encr_message = ""
    for ch in message:
        if 64 < ord(ch) and ord(ch) < 91:
            if 64 < ord(ch) + k and ord(ch) + k < 91:
                encr_message += chr(ord(ch) + k)
            else:
                encr_message += chr(ord(ch) + k - 26)
        elif 96 < ord(ch) and ord(ch) < 123:
            if 96 < ord(ch) + k and ord(ch) + k < 123:
                encr_message += chr(ord(ch) + k)
            else:
                encr_message += chr(ord(ch) + k - 26)
        else:
            encr_message += ch
    print("ciphertext:", encr_message)


if __name__ == "__main__":
    main()
