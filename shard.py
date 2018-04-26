import socket
import threading
import os
import io
from random import randint
import sys
import pickle
import time
from initial import script_dir, slaveAddrs, masterListenFromSlaveAddr, recvAll, msgLength




queryNum = 0

def listen_answer():
    listen = socket.socket()
    listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen.bind(masterListenFromSlaveAddr)
    listen.listen(12)
    while True:
        t, addr = listen.accept()
        threading.Thread(target=on_new_answer, args=(t,)).start()


def on_new_answer(command):
    while True:
        msg = recvAll(command, msgLength)
        if (msg != b''):
            file = io.BytesIO(msg)
            while True:
                try:
                    entry = pickle.load(file)
                    print(entry)
                except EOFError:
                    break

def query(start,end):
    for addr in slaveAddrs:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((socket.gethostname(), randint(30000, 40000)))
        s.connect(addr)
        message = pickle.dumps(("query", start, end))
        s.sendall(message)
    # queryNum += 1


if __name__ == "__main__":
    threading.Thread(target=listen_answer, args=()).start()
    time.sleep(0.1)
    os.system('bash slave.sh xh3426 10')
    time.sleep(20)
    if len(sys.argv) > 1:
        query(*(eval(s) for s in sys.argv[1:]))
    query(4000000, 4000999)
