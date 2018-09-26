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
    packet_encrypted = p.ProtocolEncrypted.from_string(data.decode())
    packet = packet_encrypted.decrypt(key)

    if packet.id != str(message_count):
        raise ValueError('Message count', packet.id, "doesn't match")

    message_count += 1
    data = packet.data
    print('Got ', data)
