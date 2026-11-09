import json
import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

from crypto import derive_key, new_salt, SALT_SIZE


class WrongPasswordError(Exception):
    pass


class Vault:
    def __init__(self, path="vault.bin"):
        self.path = Path(path)
        self.data = {}          # {service: {"username": ..., "password": ...}}
        self._fernet = None
        self._salt = None

    def exists(self):
        return self.path.exists()

    def create(self, master_password):
        self._salt = new_salt()
        self._fernet = Fernet(derive_key(master_password, self._salt))
        self.data = {}
        self.save()

    def unlock(self, master_password):
        raw = self.path.read_bytes()
        self._salt, token = raw[:SALT_SIZE], raw[SALT_SIZE:]
        self._fernet = Fernet(derive_key(master_password, self._salt))
        try:
            decrypted = self._fernet.decrypt(token)
        except InvalidToken:
            raise WrongPasswordError("Wrong master password or corrupted vault")
        self.data = json.loads(decrypted.decode("utf-8"))

    def save(self):
        token = self._fernet.encrypt(json.dumps(self.data).encode("utf-8"))
        # Write to a temp file first so a crash can't corrupt the vault
        tmp = self.path.with_suffix(".tmp")
        tmp.write_bytes(self._salt + token)
        os.replace(tmp, self.path)
        try:
            os.chmod(self.path, 0o600)   # owner-only (no effect on Windows)
        except OSError:
            pass

    def add(self, service, username, password):
        self.data[service.lower()] = {"username": username, "password": password}
        self.save()

    def get(self, service):
        return self.data.get(service.lower())

    def list_services(self):
        return sorted(self.data)

    def delete(self, service):
        if self.data.pop(service.lower(), None) is not None:
            self.save()
            return True
        return False