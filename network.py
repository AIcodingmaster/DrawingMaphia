import socket
from socket import error as SocketError
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
            try:
                chunk=conn.recv(4096)
                if not chunk:
                    break
                data_b+=chunk
                data=loads(data_b)
            except EOFError:#pickle 모듈 에러
                continue
            except ConnectionResetError:#client connection 끊는 에러(비정상 종료시)
                p=PlayerPacket()
                p.roomout_flag=True
                return p
            break
        return data
    def send(self,data,conn):
        conn.sendall(dumps(data))
    def close(self,conn):
        conn.close()