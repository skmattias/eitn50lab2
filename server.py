import socket
import dh
import protocol as p


IP = '127.0.0.1'
PORT = 2222
print('Waiting for key exchange on IP: ', IP, ' and port:', PORT)
key = dh.DiffieHellman().wait_for_handshake(IP, PORT)
key = key.to_bytes(32, 'big')
print('Shook hands!')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((IP, PORT))

message_count = 0
while True:
    print('Waiting for message', message_count)
    data, address = s.recvfrom(1024)
    data = p.decrypt(data, key)
    data = p.from_string(data, message_count)
    message_count += 1
    data = data.data
    print('Got ', data)
