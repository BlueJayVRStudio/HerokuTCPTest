import json

import socket
import time
from threading import Thread
from threading import Lock
from queue import Queue

class Player:
    def __init__(self, room_key, username, password):
        self.room_key = room_key
        self.username = username
        self.password = password

class Message:
    def __init__(self, username, message):
        self.username = username
        self.message = message

class RoomContext:
    def __init__(self):
        ## { 'demo_player' : (_thread, Connection) }
        self.players = { }
        self.lock = Lock()
        
    
    def ListenHandler(self, Connection):
        while (True):
            try:
                data = Connection.recv(1024)
            except:
                "player diconnected :("
                break
            data1 = data.decode()
            player_message = json.loads(data1)
            with self.lock:
                for username, (_target, connection) in self.players.items():
                    if username != player_message.username:
                        connection.send(data)

            # func("Server: " + data.decode())
    
    def connect_player(self, username, Connection):
        if username in self.players:
            return "user name already taken"
        
        _target = Thread(target=self.ListenHandler, args=(Connection))
        _target.daemon = True
        _target.start()

        self.players[username] = (_target, Connection)
        return "success"