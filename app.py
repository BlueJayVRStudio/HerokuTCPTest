#!/usr/bin/env python3

import requests
import json
from flask import Flask, request, render_template

import os

import socket
import time
from threading import Thread
from threading import Lock

from room_context import RoomContext
from room_context import Player
from room_context import Message

app = Flask(__name__)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = os.getenv('SERVER_ADDR')
s.bind((server_addr, 5000))
s.listen(5)

## Hosted Rooms = { "room key" : room context }
rooms = { }
rooms_lock = Lock()
## Waiting connections = { "room key" : connection }
connections = { }

def handle_connections():
    while (True):
        connection, client_address = s.accept()
        print(client_address)
        try:
            data = connection.recv(1024)
        except:
            print(f"could not connect player from {client_address}")
            continue
        data1 = data.decode()
        player = Player.from_json(data1)
        with rooms_lock:
            if player.room_key not in rooms:
                connection.send("could not join the room, please try again")
                continue

            connection.send(rooms[player.room_key].connect_player(player.username, connection))

_target = handle_connections
t1 = Thread(target=_target, args=())
t1.daemon = True
t1.start()

# @app.route("/", methods=["POST"])
# def main():
#     room_key = request.form.get("room_key", "")
#     username = request.form.get("username", "")
#     password = request.form.get("password", "")

#     if "room_key" not in rooms:
#         return "room not available"

#     if rooms[room_key].room_dead:
#         return "room expired"
#     else: 
#         if not rooms[room_key].started:
#             target = rooms[room_key].room_loop
#             room_thread = Thread(target=target, args=())
#             room_thread.daemon = True
#             room_thread.start()
        
#         rooms[room_key].queue.put(Player(room_key,username,password))
    
#     return "connecting..."

@app.route("/genkey", methods=["GET"])
def generate_key():
    with rooms_lock:
        key = "demoKey"
        while key in rooms:
            key = "demoKey"
        rooms[key] = RoomContext()
    time.sleep(0.05)
    return key

if __name__ == "__main__":
    # localhost
    app.run(host=server_addr, port=5100, debug=False)

