import socket
import _thread
import time
import protocol as p

IP = '127.0.0.1'
PORT = 1111
cache = []  # type: [((str, int), bytes)]


def read_data():
    """
    Receives messages from a client and saves them to a buffer.
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((IP, PORT))

    while True:
        data, address = s.recvfrom(1024)
        packet = p.ProtocolEncrypted.from_string(data.decode())
        cache.append(((packet.ip, packet.port), data))
        print('Received message')


def send_data():
    """
    Sleeps for 5 seconds, then sends all cahced messages to the server.
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        time.sleep(5)
        for data in cache:
            print('Sending packet to', ':'.join([data[0][0], str(data[0][1])]))
            s.sendto(data[1], data[0])
        cache.clear()


print('Cache server started')
_thread.start_new_thread(read_data, ())
_thread.start_new_thread(send_data(), ())

while True:
    pass
