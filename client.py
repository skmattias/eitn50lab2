import socket
import dh
import protocol as p

IP = '127.0.0.1'
CACHE_PORT = 1111
SERVER_PORT = 2222
key = dh.DiffieHellman().handshake(IP, SERVER_PORT)
key = key.to_bytes(32, 'big')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message_count = 0
while True:
    message = input("Enter message: ")
    packet = p.Protocol(message_count, message)
    message_count += 1
    encrypted = packet.encrypt(key)
    s.sendto(encrypted, (IP, CACHE_PORT))
    print(message, 'sent!')
