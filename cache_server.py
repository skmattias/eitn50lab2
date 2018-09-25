import socket
import _thread
import time

IP = '127.0.0.1'
PORT = 1111
SERVER_PORT = 2222
cache = []
print('Cache server started')


def read_data():
    """
    Receives messages from a client and saves them to a buffer.
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((IP, PORT))

    while True:
        data, address = s.recvfrom(1024)
        cache.append(data)
        print('Received message')


def send_data():
    """
    Sleeps for 5 seconds, then sends all cahced messages to the server.
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        time.sleep(5)
        print('Sending', len(cache), 'packets')
        for data in cache:
            s.sendto(data, (IP, SERVER_PORT))
        cache.clear()


try:
    _thread.start_new_thread(read_data, ())
    _thread.start_new_thread(send_data(), ())
except:
    print("Error: unable to start thread")

while True:
    pass
