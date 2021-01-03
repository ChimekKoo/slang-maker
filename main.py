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
    with open("config.json", "r") as config_file:
        config = loads(config_file.read())
        config_file.close()
except FileExistsError:
    print("ERROR: config.json file does not exists.")
    exit(1)

psw = input("Password: ")

if not verify_password(config["password-hash"], psw):
    print("Wrong password.")
    exit(1)

try:
    with open(config["file-path"], "r") as slang_file:
        try:
            slang = loads(slang_file.read())
            slang_file.close()
        except JSONDecodeError:
            print(f"ERROR: Error in decoding JSON in {config['file-path']} file.")
            exit(1)
except FileExistsError:
    print(f"ERROR: {config['file-path']} file does not exists.")
    exit(1)

while True:
    a = input("Type sentence or 'q' to quit: ")
    if a == "q":
        break
    else:
        for word in slang.keys():
            if word in a:
                a = a.replace(word, choice(slang[word]))
        print("\nSentence in slang:", a)
