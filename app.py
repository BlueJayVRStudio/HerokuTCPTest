#!/usr/bin/env python3

import requests
import json
from flask import Flask, request, render_template

import socket
import time
from threading import Thread

# app = Flask(__name__)

# def socketThread():
#     # Create a socket object
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # Bind the socket to a specific network interface and port number
#     s.bind(('147.182.204.67', 5000))

#     # Listen for incoming connections
#     s.listen(5)

#     counter = 100
#     print("hello world! we are now starting a TCP server!")
#     while (True):
#         print("this is the loop")
#         counter -= 1
#         # Accept an incoming connection
#         connection, client_address = s.accept()
#         print(client_address)
#         # Send and receive data
#         connection.send('Hello, world!'.encode())
#         data = connection.recv(1024)

#         # Start a Send thread and a Receive thread


#         print(data.decode())

#         # # Close the socket
#         connection.close()
# # t1 = Thread(target=socketThread, args=())
# # t1.start()

# socketThread()

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
server_socket.bind(("147.182.204.67", 5001))

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific network interface and port number
s.bind(('147.182.204.67', 5000))

# Listen for incoming connections
s.listen(5)

# Listen for messages
while True:
  connection, client_address = s.accept()
  print(client_address)
  data = connection.recv(1024)
  
  data1, client_address1 = server_socket.recvfrom(1024)

#   # Print the message
  print("Received message from {}: {}".format(client_address, data))
  print("Received message from {}: {}".format(client_address1, data1))

  # Send a response back to the client
  server_socket.sendto("Received!".encode(), client_address)



# @app.route("/", methods=["POST", "GET"])
# def main():
#     input_text = request.form.get("user_input", "")
#     input_text1 = request.form.get("user_input1", "")

#     return "hehehehe"

#     return f"You entered: {input_text} AND {input_text1}!"

# @app.route("/healthcheck", methods=["GET"])
# def healthcheck():
#     return "healthy"

# if __name__ == "__main__":
#     # localhost
#     app.run(host= '0.0.0.0', port=5100, debug=False)

