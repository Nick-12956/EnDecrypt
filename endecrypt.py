# --------------------<<< ENDECRYPT >>>--------------------

# ----------< Libraries >----------

from cryptography.fernet import Fernet, InvalidToken
import tkinter as tk
from tkinter import filedialog
import os

# ----------< Constants >----------

RED = "\033[31m"
GREEN = "\033[32m"
LIGHT_BLUE = "\033[94m"
ORANGE = "\033[38;5;208m"
PURPLE = "\033[35m"
RESET = "\033[0m"

# ----------< Functions >----------

# -----< File location >-----

def locate_file(file_path: str) -> str:
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All Files", "*.*")]
    )
    root.destroy()
    if file_path:
        return os.path.normpath(file_path)
    return ""

# -----< Key >-----

def generate_key():
    key = Fernet.generate_key()
    return key

def is_valid_key(key_input: bytes) -> bool:
    try:
        Fernet(key_input)
        return True
    except Exception:
        return False

# -----< Crypto >-----

def encrypt_message(message: str, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def encrypt_file(file_path: str, key: bytes) -> None:
    f = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = f.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file(file_path: str, key: bytes) -> None:
    f = Fernet(key)
    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = f.decrypt(encrypted)
    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

# ---------------------------------

# ----------< MAIN >----------

if __name__ == "__main__":

    print(f"{ORANGE}--------------------<<< ENDECRYPT >>>--------------------{RESET}\n")
    print(f"{RED}!! Copy the \"KEY\" when printed as it is not stored (Without it, you cannot decrypt data){RESET}")
    while True:
        print(f"{ORANGE}\n---------------<<< MENU >>>---------------{RESET}\n")
        print(f"{LIGHT_BLUE}1. Encrypt a message{RESET}")
        print(f"{LIGHT_BLUE}2. Decrypt a message{RESET}")
        print(f"{LIGHT_BLUE}3. Encrypt a file{RESET}")
        print(f"{LIGHT_BLUE}4. Decrypt a file{RESET}")
        print(f"{LIGHT_BLUE}5. Exit{RESET}")
        option = input(f"{PURPLE}Enter Option : {RESET}").strip()
        if option == "1":
            lines = []
            print(f"{PURPLE}---< Enter the message to encrypt (type 'stop' on a new line to exit) >---{RESET}")
            while True:
                user_input = input()
                if user_input.strip() == "stop":
                    break
                lines.append(user_input)
            message = "\n".join(lines)
            key = generate_key()
            encrypted_message = encrypt_message(message, key)
            print(f"\n{ORANGE}Key: {RESET}{key.decode()}")
            print(f"\n{GREEN}Encrypted Message:{RESET}\n{encrypted_message.decode()}\n")
        elif option == "2":
            input_key = input(f"{PURPLE}===> Enter key : {RESET}").strip().encode()
            if not is_valid_key(input_key):
                print(f"{RED}Invalid key. Please try again.{RESET}")
                continue
            encrypted_message = input(
                f"{PURPLE}---< Enter the encrypted message >---\n{RESET}"
            ).strip().encode()
            try:
                decrypted_message = decrypt_message(encrypted_message, input_key)
                print(f"\n{GREEN}Decrypted Message:{RESET}\n{decrypted_message}\n")
            except ValueError:
                print(f"{RED}The key or encrypted message contains invalid characters.{RESET}")
            except Exception as e:
                print(f"{RED}Decryption failed: {e}{RESET}")
        elif option == "3":
            print(f"{PURPLE}---< Select a file to encrypt >---{RESET}")
            file_path = locate_file("")
            if not file_path:
                print(f"{RED}No file selected.{RESET}")
                continue
            try:
                key = generate_key()
                encrypt_file(file_path, key)
                print(f"\n{GREEN}File encrypted successfully:{RESET} {file_path}")
                print(f"{ORANGE}Key: {RESET}{key.decode()}\n")
            except (OSError, ValueError) as e:
                print(f"{RED}File encryption failed: {e}{RESET}")
        elif option == "4":
            print(f"{PURPLE}---< Select a file to decrypt >---{RESET}")
            file_path = locate_file("")
            if not file_path:
                print(f"{RED}No file selected.{RESET}")
                continue
            input_key = input(f"{PURPLE}===> Enter key : {RESET}").strip().encode()
            if not is_valid_key(input_key):
                print(f"{RED}Invalid key. Please try again.{RESET}")
                continue
            try:
                decrypt_file(file_path, input_key)
                print(f"\n{GREEN}File decrypted successfully:{RESET} {file_path}\n")
            except InvalidToken:
                print(f"{RED}File decryption failed: invalid key or encrypted file.{RESET}")
            except (OSError, ValueError) as e:
                print(f"{RED}File decryption failed: {e}{RESET}")
        elif option == "5":
            print(f"{ORANGE}\n---------------<<< EXIT >>>---------------{RESET}\n")
            break
        else:
            print(f"{RED}Invalid option. Please try again.{RESET}")
