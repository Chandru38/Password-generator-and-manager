# Password Generator and Manager

A command-line tool that generates strong random passwords and stores
them in an encrypted vault protected by a master password.

## Features
- Cryptographically secure password generation (`secrets`)
- Encrypted storage using Fernet (`cryptography`)
- Master password key derivation with PBKDF2 (600,000 iterations)
- Add, view, list and delete entries

## Setup
```bash
git clone https://github.com/Chandru38/Password-manager.git
cd Password-manager
pip install -r requirements.txt
python main.py
```

On first run it creates a new encrypted `vault.bin` locally.

## Note
This is a learning project, not a replacement for a vetted password manager.

## Working
Note that getpass doesn’t show anything as you type the master password. That’s intentional, so just type it and press Enter.

## Try the walkthrough
Note:Type the number at the > prompt and press Enter.
1. Add an entry: type 2, then enter gmail as the service and your email as the username. At the password prompt, press Enter without typing anything to auto-generate one. The generated password is printed so you can copy it.
2. List services: type 4. You should see - gmail.
3. Get an entry: type 3, then gmail. It prints the username and password.
4. Quit: type 6.
