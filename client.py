import socket
import dh
import protocol as p

IP = '127.0.0.1'
PORT = 6789
key = dh.DiffieHellman().handshake(IP, PORT)
key = key.to_bytes(32, 'big')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

c = True
message_count = 0
while c:
    message = input("Enter message...")
    packet = p.Protocol(message_count, message)
    message_count += 1
    encrypted = packet.encrypt(key)

    s.sendto(encrypted, (IP, PORT))

    if message == 'exit':
        print('Exiting')
        c = False
