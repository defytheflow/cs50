# Cracks the password which had been crypted using UNIX crypt function.
import sys
import string
import time
import array
import itertools

import crypt


def main():
    check_args()
    salt_hash = sys.argv[1]
    password = crack(salt_hash)
    print(password)


def check_args():
    """ Checks provided command lines arguments. """
    if not len(sys.argv) == 2:
        print("Usage caesar.py k")
        sys.exit(1)
    if len(sys.argv[1]) != 13:
        print("Incorrect Hash Value.")
        sys.exit(1)


def crack(salt_hash:str):
    """ Cracks the password using using UNIX crypt function"""
    #bad_tries = []
    salt = salt_hash[:2]
    for i in range(1, 6):
        alpha = array.array("u", string.ascii_letters)
        combinations = tuple([alpha for j in range(i)])
        #if i > 3:
        #    with open("passwords.txt", "r") as f:
        #        for password in f:
        #            password = password.rstrip()
        #            guess = crypt.crypt(password, salt)
        #            if guess == salt_hash:
        #                return password
        #            else:
        #               bad_tries.append(password)
        for comb in itertools.product(*combinations):
            #if comb in bad_tries:
            #    continue
            password = "".join(comb)
            guess = crypt.crypt(password, salt)
            if guess == salt_hash:
                return password


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")
