from network import Net
from _thread import *
from model import *
#addr=('localhost',5555)
addr=('172.26.10.205',5556)

rooms_lock=allocate_lock()
class Server:
    def __init__(self,addr):
        self.net=Net()
        self.net.init_server(addr,LISTEN_NUM)
        self.rooms=[]
    def make_room(self,room,c):
        rooms_lock.acquire()
        room.code=room.get_code()
        self.rooms.append(room)
        rooms_lock.release()
        self.net.send(room.getPacket(),c)
        left_p_num=room.start_room(c,self.net)
        if left_p_num==0:
            rooms_lock.acquire()
            Room.room_code[room.code]=True
            self.rooms.remove(room)
            rooms_lock.release()
    def code_find_room(self,code,c):
        print(code)
        for room in self.rooms:
            rooms_lock.acquire() 
            if str(room.code)==code.strip() and not room.start_flag and room.total_p_num>room.p_num:
                player_code=room.add_player()
                rooms_lock.release()
                self.net.send(player_code,c)
                self.net.send(room.getPacket(),c)
                left_p_num=room.start_room(c,self.net)
                if left_p_num==0:
                    rooms_lock.acquire()
                    Room.room_code[room.code]=True
                    self.rooms.remove(room)
                    rooms_lock.release()
                return
            rooms_lock.release()
        self.net.send(-1,c)
        self.net.send(-1,c)
    def find_room(self,num,c):
        for room in self.rooms:
            rooms_lock.acquire()
            if room.total_p_num==num and room.total_p_num>room.p_num and not room.start_flag:#num명 방이고 인원이 다 안찼으면
                player_code=room.add_player()
                rooms_lock.release()
                self.net.send(player_code,c)
                self.net.send(room.getPacket(),c)
                left_p_num=room.start_room(c,self.net)
                if left_p_num==0:
                    rooms_lock.acquire()
                    Room.room_code[room.code]=True
                    self.rooms.remove(room)
                    rooms_lock.release()
                return
            rooms_lock.release()
        room=Room(num)
        rooms_lock.acquire()
        room.code=room.get_code()
        self.rooms.append(room)
        rooms_lock.release()
        self.net.send(0,c)
        self.net.send(room.getPacket(),c)
        left_p_num=room.start_room(c,self.net)
        if left_p_num==0:
            rooms_lock.acquire()
            Room.room_code[room.code]=True
            self.rooms.remove(room)
            rooms_lock.release()
    def run(self):
        print("Server is running")
        while True:
            c, address = self.net.accept()
            start_new_thread(self.client, (c,))#thread
    def client(self,c):
        while True:
            data=self.net.recv(c)
            if not data:#연결이 끊어졌다면 thread 탈출
                #print('normal exit')
                break
            r_data=self.make_find_room(c,data)
            if type(r_data)==PlayerPacket:
                #print("abnormal exit")
                break
        self.net.close(c)
    def make_find_room(self,c,data):
        if data=="f4":
            self.find_room(4,c)
        elif data=="f8":
            self.find_room(8,c)
        elif data=="m4":
            room=Room(4)
            self.make_room(room,c)
        elif data=="m8":
            room=Room(8)
            self.make_room(room,c)
        elif type(data)!=PlayerPacket:
            self.code_find_room(data,c)
        else:
            return data
server=Server(addr)
server.run()
