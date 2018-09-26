import binascii
from Crypto.Cipher import AES


iv = '0123456789ABCDEF'
delimiter = '%'
pad_character = '#'


def pad_to_16(s: str):
    extra = 16 - (len(s) % 16)
    if extra > 0:
        s = s + (pad_character * extra)
    return s


class Protocol:
    def __init__(self, ip: str, port: int, id: int, data: str):
        self.ip = ip
        self.port = port
        self.id = str(id)
        self.data = data
        self.crc = str(binascii.crc32(data.encode()))

    def encrypt(self, key: bytes):
        aes = AES.new(key, AES.MODE_CBC, iv)
        to_encrypt = delimiter.join([self.id, self.data, self.crc])
        to_encrypt = pad_to_16(to_encrypt)
        payload = aes.encrypt(to_encrypt)
        return ProtocolEncrypted(self.ip, self.port, payload)


class ProtocolEncrypted:
    def __init__(self, ip: str, port: int, payload: bytes):
        self.ip = ip
        self.port = port
        self.payload = payload

    def decrypt(self, key: bytes):
        aes = AES.new(key, AES.MODE_CBC, iv)
        payload = aes.decrypt(self.payload).decode()
        payload = payload.replace(pad_character, '')
        payload = payload.split(delimiter)  # type: [str]
        id = int(payload[0])
        data = payload[1]
        crc = payload[2]
        protocol = Protocol(self.ip, self.port, id, data)

        if crc != protocol.crc:
            raise ValueError("CRC doesn't match")

        return protocol

    def to_string(self):
        """
        Structure:
        destination_ip%destination_port%payload,
        where payload is encrypted.
        """
        return delimiter.join([self.ip, str(self.port), self.payload.hex()])

    @staticmethod
    def from_string(obj: str):
        obj = obj.split(delimiter)  # type: [str]
        return ProtocolEncrypted(obj[0], int(obj[1]), bytes.fromhex(obj[2]))
