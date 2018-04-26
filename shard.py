import socket
import threading
import os
from random import randint
import sys
import pickle
import time
from initial import script_dir, slaveAddrs, masterListenFromSlaveAddr




def on_new_answer():
    listen = socket.socket()
    listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen.bind(masterListenFromSlaveAddr)
    listen.listen(12)
    while True:
        t, addre = listen.accept()
        msg = t.recv(1024)
        print(pickle.loads(msg))

def query(start,end):

    for addr in slaveAddrs:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((socket.gethostname(), randint(30000, 40000)))
        s.connect(addr)
        message = pickle.dumps(("query", start, end))
        s.sendall(message)


if __name__ == "__main__":
    threading.Thread(target=on_new_answer, args=()).start()
    time.sleep(0.1)
    os.system('bash slave.sh xh3426 10')
    time.sleep(20)
    if len(sys.argv) > 1:
        query(*(eval(s) for s in sys.argv[1:]))
    query(4000000, 4000999)
