from json import loads
from json.decoder import JSONDecodeError
from random import choice
import hashlib
import binascii
import os


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


try:
    f = input("Slang file path: ")

    try:
        with open(f, "r") as config_file:
            try:
                config = loads(config_file.read())
                config_file.close()
            except JSONDecodeError:
                print("ERROR: JSON decode error.")
                exit(1)
    except FileNotFoundError:
        print(f"ERROR: {f} file does not exists.")
        exit(1)

    psw = input("Password: ")

    if not verify_password(config["password-hash"], psw):
        print("Wrong password.")
        exit(1)

    slang = config["words"]
except KeyboardInterrupt:
    exit(0)

while True:
    try:
        a = input("Type sentence or 'q' to quit: ")
        if a == "q":
            break
        else:
            for word in slang.keys():
                if word in a:
                    if not isinstance(slang[word], list):
                        print("ERROR: JSON decode error.")
                        exit(1)
                    a = a.replace(word, choice(slang[word]))
            print("\nSentence in slang:", a)
    except KeyboardInterrupt:
        exit(0)
