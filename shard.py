import socket
import threading

from random import randint
import sys
import pickle
import time
from initial import script_dir, slaveAddrs



listenAddr = (socket.gethostname(), randint(30000, 40000))
print(listenAddr)

def on_new_answer(addr):
    listen = socket.socket()
    listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen.bind(listenAddr)
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
        print(addr)
        s.connect(addr)
        message = pickle.dumps(("query", start, end, listenAddr))
        s.sendall(message)


if __name__ == "__main__":
    threading.Thread(target=on_new_answer, args=(listenAddr,)).start()
    time.sleep(0.2)
    if len(sys.argv) > 1:
        s = query(*(eval(s) for s in sys.argv[1:]))
    query(4000000, 4000999)
