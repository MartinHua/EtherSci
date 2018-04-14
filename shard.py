import socket
import threading
from client import shard_client
from random import randint
import time
from ctypes import c_int, addressof
import pickle
import sys
import os
serverPort = randint(2000,26000)

servers = [-1]*5
clients = [-1]*10
clientPort = randint(30000, 40000)
masterPort = randint(26002, 29999)
connectedSids = [[],[],[],[],[]]
clientConnected = [-1]*10

c = client(cid, clientPort - cid, sport(sid))