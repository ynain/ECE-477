#!/usr/bin/env python3

import socket

HOST = '128.46.96.231'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("Waiting for...")
    conn, addr = s.accept()
    print("connection on {}:{}".format(HOST, PORT))

    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
