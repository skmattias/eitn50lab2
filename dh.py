from Crypto import Random
import socket


class DiffieHellman:
    p = 5821
    g = 2

    def handshake(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        a = int.from_bytes(Random.new().read(16), 'big')
        A = pow(self.g, a, self.p)
        s.sendto(str(A).encode(), (ip, port))
        B, server = s.recvfrom(1024)
        B = int(B.decode())
        return pow(B, a, self.p)

    def wait_for_handshake(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((ip, port))
        A, address = s.recvfrom(1024)
        A = int(A.decode())
        b = int.from_bytes(Random.new().read(16), 'big')
        B = pow(self.g, b, self.p)
        s.sendto(str(B).encode(), address)
        return pow(A, b, self.p)
