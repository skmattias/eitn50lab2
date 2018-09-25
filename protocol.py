import binascii
from Crypto.Cipher import AES


iv = '0123456789ABCDEF'
deliminator = '%'
pad_character = '#'


def pad_to_16(s: str):
    extra = 16 - (len(s) % 16)
    if extra > 0:
        s = s + (pad_character * extra)
    return s


def decrypt(obj: str, key: bytes):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(obj).decode()


def from_string(obj: str, expected_number: int):
    obj = obj.replace(pad_character, '')
    vector = obj.split(deliminator)
    protocol = Protocol(int(vector[0]), vector[1])

    if vector[2] != protocol.crc:
        raise ConnectionError("CRC doesn't match")

    if int(vector[0]) != expected_number:
        raise ValueError("REPLAY ATTACK")

    return protocol


class Protocol:
    def __init__(self, id: int, data: str):
        self.id = str(id)
        self.data = data
        self.crc = str(binascii.crc32(data.encode()))

    def to_string(self):
        return deliminator.join([self.id, self.data, self.crc])

    def encrypt(self, key: bytes):
        aes = AES.new(key, AES.MODE_CBC, iv)
        to_encrypt = self.to_string()
        to_encrypt = pad_to_16(to_encrypt)
        return aes.encrypt(to_encrypt)
