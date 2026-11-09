from getpass import getpass
# getpass = input

from generator import generate_password
from vault import Vault, WrongPasswordError

MENU = """
1) Generate a password
2) Add an entry (generate or enter)
3) Get an entry
4) List services
5) Delete an entry
6) Quit
"""

def open_vault():
    vault = Vault()
    if not vault.exists():
        print("No vault found. Let's create one.")
        while True:
            pw = getpass("Choose a master password: ")
            if len(pw) < 12:
                print("Use at least 12 characters.")
                continue
            if pw != getpass("Confirm: "):
                print("Passwords don't match.")
                continue
            break
        vault.create(pw)
        print("Vault created.")
    else:
        try:
            vault.unlock(getpass("Master password: "))
        except WrongPasswordError as e:
            print(e)
            raise SystemExit(1)
    return vault

def main():
    vault = open_vault()
    while True:
        print(MENU)
        choice = input("> ").strip()

        if choice == "1":
            length = int(input("Length [16]: ") or 16)
            print(generate_password(length))

        elif choice == "2":
            service = input("Service: ").strip()
            username = input("Username/email: ").strip()
            pw = getpass("Password (leave blank to generate): ")
            if not pw:
                pw = generate_password()
                print(f"Generated: {pw}")
            vault.add(service, username, pw)
            print("Saved.")

        elif choice == "3":
            entry = vault.get(input("Service: "))
            if entry:
                print(f"Username: {entry['username']}")
                print(f"Password: {entry['password']}")
            else:
                print("Not found.")

        elif choice == "4":
            for s in vault.list_services():
                print(" -", s)

        elif choice == "5":
            print("Deleted." if vault.delete(input("Service: ")) else "Not found.")

        elif choice == "6":
            break


if __name__ == "__main__":
    main()
