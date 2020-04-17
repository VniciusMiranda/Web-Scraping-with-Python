import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encryptPassword(password, storePassword):
    pass


def createKey(password_provided=None):
    if password_provided is not None:
        password = password_provided.encode()  # Convert to type bytes
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once

    else:
        return Fernet.generate_key()


def storeKey(key, path):
    with open(path, 'w+') as file:
        file.write(key)


def encrypt():

    bye = False
    while not bye:
        print("="*60)
        print("\n")
        print("WELCOME")
        print("This is a python program to encrypt passwords base on key (symmetric cryptography).")
        print("\n")
        print("="*60)
        print("\n")
        while True:
            print("The key will be randomly generated or base on a word?")
            print("0 - cancel")
            print("1 - randomly generated")
            print("2 - base on a word")
            option = int(input(">"))
            if option not in [0, 1, 2]:
                print("invalid input!")
                print("try again...")
            else:
                print("-"*60)
                if option == 0:
                    bye = True
                    print("bye...")
                if option == 1:
                    key = createKey()
                if option == 2:
                    encryptWord = input("enter the encryption word:")
                    key = createKey(encryptWord)
                break

        print("key successfully created.")
        print("-" * 60)
        print("enter the path to store the key:")
        print("(or just the name of the file,\nin this case it will be stored at the same directory as this file)")
        storePath = input(">")

        storeKey(key, storePath)
        print("key successfully stored.")


if "__main__" == __name__:
    encrypt()
