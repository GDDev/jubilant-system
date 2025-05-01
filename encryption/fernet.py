from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os


load_dotenv()


class FernetEncrypter:

    def __init__(self):
        self.key = self.load_key()
        self.fernet = Fernet(self.key)

    @staticmethod
    def load_key() -> bytes:
        key = os.getenv("MASTER_ENCRYPTION_KEY")
        if not key:
            raise ValueError("MASTER_ENCRYPTION_KEY not found in environment variables.")
        return key.encode()

    def encrypt(self, message: str | bytes) -> bytes:
        if isinstance(message, str):
            message = message.encode()
        return self.fernet.encrypt(message)

    def decrypt(self, token: bytes) -> str | bytes:
        decrypted = self.fernet.decrypt(token)
        try:
            return decrypted.decode()
        except UnicodeDecodeError:
            return decrypted