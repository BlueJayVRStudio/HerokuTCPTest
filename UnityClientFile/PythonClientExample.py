import os
import json

import socket
import time
from threading import Thread

SERVER_ADDR = os.getenv('SERVER_ADDR')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
t1 = time.time()

s.connect((SERVER_ADDR, 5001))
time.sleep(0.06)
print((time.time()-t1)*1000)

