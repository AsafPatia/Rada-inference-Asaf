import logging
from datetime import datetime
import time
from config.settings import settings
from utils.BMAsyncSocket import BMAsyncSocket



def handle_message_received_callback(data):
    assert data is not None
    print(datetime.now(), 'handling message received: ', data)


def test_socket_localhost():
    listener = BMAsyncSocket("localhost", 7033, handle_message_received_callback)
    listener.start()
    time.sleep(1)
    BMAsyncSocket.send_msg("localhost", 7033, "localhost".encode())
    time.sleep(1)
    listener.stop()

    listener = BMAsyncSocket("127.0.0.1", 7033, handle_message_received_callback)
    listener.start()
    time.sleep(1)
    BMAsyncSocket.send_msg("127.0.0.1", 7033, "127.0.0.1".encode())
    time.sleep(1)
    listener.stop()

    result = True
    assert result is True


def test_socket_receive():
    listener = BMAsyncSocket(settings.host_ip, settings.host_port, handle_message_received_callback)
    listener.start()
    time.sleep(1)
    counter = 1
    while counter < 4:
        BMAsyncSocket.send_msg(settings.host_ip, settings.host_port, ("Hello " + str(counter)).encode())
        counter += 1
        time.sleep(1)

    listener.stop()
    result = True
    assert result is True
