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
    def to_json(self):
        _json = {
            'room_key' : self.room_key,
            'username' : self.username,
            'password' : self.password
        }
        return _json
    
    def from_json(self, _json):
        loaded = json.loads(_json)
        self.room_key = loaded['room_key']
        self.username = loaded['username']
        self.password = loaded['password']
        return self

class Message:
    def __init__(self, username, message):
        self.username = username
        self.message = message
    
    def to_json(self):
        _json = {
            'username' : self.username,
            'message' : self.message
        }
        return _json
    
    def from_json(self, _json):
        # print(_json)
        loaded = json.loads(_json)
        self.username = loaded['username']
        self.message = loaded['message']
        return self

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
                print("player diconnected :(")
                break
            data1 = data.decode()
            # print(data1)
            try:
                player_message = Message(None, None).from_json(data1)
            except:
                print("error handling message. disconnecting player...")
                break
            with self.lock:
                for username, (_target, connection) in self.players.items():
                    if username != player_message.username:
                        connection.send(data)

            # func("Server: " + data.decode("utf-8"))
    
    def connect_player(self, username, Connection):
        if username in self.players:
            return "user name already taken"
        
        _target = Thread(target=self.ListenHandler, args=(Connection,))
        _target.daemon = True
        _target.start()

        self.players[username] = (_target, Connection)
        return "success"