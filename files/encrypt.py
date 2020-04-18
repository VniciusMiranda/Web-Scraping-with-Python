import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def optionSelector(question: str, options: dict, lineChar='-') -> int:
    while True:
        print(lineChar*60)
        print(question)
        for keys, values in options.items():
            print(f"    {keys} - {values}")

        option = int(input(">"))

        if option not in list(options.keys()):
            print("invalid option!")
            print("try again...")
        else:
            break
    return option


def encryptPassword(password, keyPath):

    if os.path.exists(keyPath):
        with open(keyPath, "rb") as file:
            key = file.read()
        f = Fernet(key)
        encrypted = f.encrypt(password.encode())
        print("password encrypted successfully :)")
    else:
        encrypted = None
        print("path doesn't exists:c\nreturning None...")

    return encrypted


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


def store(info, path, bytes_=False):

    if not bytes_:
        with open(path, 'w+') as file:
            file.write(info)
    else:
        with open(path, "wb") as file:
            file.write(info)


def encrypt():
    print("=" * 60)
    print("WELCOME")
    print("This is a python program to encrypt passwords base on key (symmetric cryptography).")

    while True:
        print("=" * 60)
        mainMenuOptions = {
            0: "exit",
            1: "encrypt a password",
            2: "create a new key"
        }
        mainMenuOption = optionSelector("options:", mainMenuOptions, lineChar="")

        if mainMenuOption is 0:
            print("bye...")
            break

        if mainMenuOption is 1:
            print("-"*60)
            print("enter the password:")
            password = input(">")
            print("enter the key path:")
            keyPath = input(">")
            encryptedPassword = encryptPassword(password, keyPath)
            if encryptedPassword is None:
                print("error occurred. Returning to the main menu :/")
                input("press any key to continue...")
            else:
                print("enter the path where to store the encrypted password:")
                passwordPath = input(">")
                store(encryptedPassword, passwordPath, bytes_=True)
                print(f"encrypted password store at {passwordPath}")

        if mainMenuOption is 2:
            keyOptions = {
                0: "cancel",
                1: "randomly generated",
                2: "base on a word"
            }
            keyOption = optionSelector(
                "The key will be randomly generated or base on a word?",
                keyOptions)

            if keyOption is 0:
                print("going back...?")
                continue

            if keyOption is 1:
                key = createKey()
            if keyOption is 2:
                encryptWord = input("enter the encryption word:")
                key = createKey(encryptWord)

            print("key successfully created.")
            print("-" * 60)
            print("enter the path to store the key(extension: '.key'):")
            print("(or just the name of the file,\nin this case it will be stored at the same directory as this file)")

            while True:
                keyStorePath = input(">")
                if keyStorePath.find(".key") is not -1:
                    break

                else:
                    print("remember to add the extension.")
                    print("try again")

            store(key, keyStorePath, bytes_=True)
            print(f"key stored at {keyStorePath}")


if "__main__" == __name__:
    encrypt()
