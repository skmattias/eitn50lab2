import socket
import dh
import protocol as p

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2222
CACHE_IP = '127.0.0.1'
CACHE_PORT = 1111
key = dh.DiffieHellman().handshake(SERVER_IP, SERVER_PORT)
key = key.to_bytes(32, 'big')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message_count = 0
while True:
    message = input("Enter message: ")
    packet = p.Protocol(SERVER_IP, SERVER_PORT, message_count, message)
    message_count += 1
    encrypted = packet.encrypt(key)
    s.sendto(encrypted.to_string().encode(), (CACHE_IP, CACHE_PORT))
    print(message, 'sent!')
