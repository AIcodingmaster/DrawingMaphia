import socket
from _pickle import dumps,loads
from sys import getsizeof
from _thread import *
from model import *
import time

class Net():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def init_server(self,soc,listen):
        self.s.bind(soc)
        self.s.listen(listen)
    def init_client(self,soc):
        self.s.connect(soc)
    def accept(self):
        return self.s.accept()
    def recv(self,conn):
        data_b=b''
        data=None
        while True:
            chunk=conn.recv(4096)
            if not chunk:
                break
            data_b+=chunk
            try:
                data=loads(data_b)
            except:
                continue
            break
        return data
    def send(self,data,conn):
        conn.sendall(dumps(data))
    def close(self,conn):
        conn.close()