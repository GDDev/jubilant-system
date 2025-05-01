from secrets import token_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AESGCMEncrypter:
    def __init__(self, key):
        self.key = key
        self.aes = AESGCM(self.key)

    def encrypt(self, plaintext: str | bytes, aad: bytes = b"") -> bytes:
        if isinstance(plaintext, str): plaintext = plaintext.encode()
        nonce = token_bytes(12)
        return nonce + self.aes.encrypt(nonce, plaintext, aad)

    def decrypt(self, ciphertext: bytes, aad: bytes = b"") -> str | bytes:
        decrypted = self.aes.decrypt(ciphertext[:12], ciphertext[12:], aad)
        try:
            return decrypted.decode()
        except UnicodeDecodeError:
            return decrypted

    @staticmethod
    def generate_key() -> bytes:
        return AESGCM.generate_key(key_size=32)