#!/usr/bin/env python3

import requests
import json
from flask import Flask, request, render_template

import socket
import time
from threading import Thread

app = Flask(__name__)

def socketThread():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific network interface and port number
    s.bind(('localhost', 5000))

    # Listen for incoming connections
    s.listen(5)

    counter = 100
    print("hello world! we are now starting a TCP server!")
    while (True):
        print("this is the loop")
        counter -= 1
        # Accept an incoming connection
        connection, client_address = s.accept()
        print(client_address)
        # Send and receive data
        # connection.send('Hello, world!'.encode())
        # data = connection.recv(1024)
        # print(data.decode())

        # # Close the socket
        # connection.close()
t1 = Thread(target=socketThread, args=())
t1.start()

# socketThread()

@app.route("/", methods=["POST", "GET"])
def main():
    input_text = request.form.get("user_input", "")
    input_text1 = request.form.get("user_input1", "")

    return "hehehehe"

    return f"You entered: {input_text} AND {input_text1}!"

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return "healthy"

if __name__ == "__main__":
    # localhost
    app.run(host= '0.0.0.0', port=5100, debug=False)

