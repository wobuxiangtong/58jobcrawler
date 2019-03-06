from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES

BLOCK_SIZE = 16


class AESCipher:

    def __init__(self, key):
        self.key = key

    def pad(self, s):
        "补足16位,以填充长度对应的ascii*补充长度作为填充"
        return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

    def unpad(self, s):
        "去掉解码后的补充位"
        return s[:(-ord(s[len(s) - 1:]))]

    def encrypt(self, raw):
        raw = self.pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self.unpad(cipher.decrypt(enc)).decode('utf8')


if __name__ == "__main__":
    key = '5749812cr3419i8s'
    aes = AESCipher(key)
    en = ['VAksFcTEU31Ll8qtub4aUQ==', 'ZlgHE6vY0vjR5FRNYFm+hQ==']
    for virtualNumber in en:
        print('en:', virtualNumber)
        print('de:', aes.decrypt(virtualNumber))
