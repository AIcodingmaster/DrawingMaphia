#listen limit : 100, room limit : 100
import pygame
import random
from _thread import *
from setting import *
from functools import reduce
LISTEN_NUM=100
ROOM_NUM=30
class InputBox:#방 code로 입장 or 투표할 때 쓰는 inputbox
    def __init__(self, x, y, w, h,dm, text=''):
        self.dm=dm
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color(200,200,30)
        self.text = text
        self.font=pygame.font.SysFont(FONT_NAME,15)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color =   pygame.Color(200,200,30) if self.active else pygame.Color(240,240,15)
        if event.type == pygame.KEYDOWN:
            if self.active:
                #print(event.key)
                if event.key == pygame.K_RETURN:
                    self.dm.scene.player.voting=self.text
                    self.text = ''
                    self.dm.scene.voted=True
                elif event.key == pygame.K_BACKSPACE or event.key==271:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, BLACK)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        # Blit the rect.
        pygame.draw.rect(self.dm.screen, self.color, self.rect, 2)
        # Blit the text.
        self.dm.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
class Paper:
    def __init__(self,dm):#points = (시작점, 끝점)
        self.player_points=[list() for x in range(8)]#player code를 index로 하여 points들이 있음
        self.dm=dm
        self.difference=set()#보내야할 데이터를 그때 초기화하는 것
    def drawPoints(self,points_set,color):#points는 point(last점,end점)들의 모임, 점은 (x,y)좌표로 표현
        for last,end in points_set:
            pygame.draw.line(self.dm.screen,color,last,end,5)
    def resetPaper(self):
        self.player_points=[list() for x in range(8)]
    def event(self):
        mouses=pygame.mouse.get_pressed()
        if mouses[2] and self.dm.scene.d_active and self.dm.scene.player.canvas_catched:#캔버스를 잡았고, 오른쪽 버튼이 눌렸다면
            mouse_pos=pygame.mouse.get_pos()
            if self.dm.scene.last_pos==None:
                self.dm.scene.last_pos=mouse_pos
            if (self.dm.scene.last_pos,mouse_pos) not in self.player_points[self.dm.scene.player.code]:
                self.difference.add((self.dm.scene.last_pos,mouse_pos))
            self.dm.scene.last_pos=mouse_pos
    def getNewPoints(self):
        l=0
        #self.player_points[self.dm.scene.player.code].update(self.difference)#갱신
        for i in range(8):#paper는
            l+=len(self.dm.scene.paper.player_points[i])#플레이어가 그린 (시작점, 끝점)들을 더해 전체 길이 구함.
        paper=list(zip([self.dm.scene.player.code]*len(self.difference),list(self.difference)))# (player_code,(시작점,끝점)) 를 원소로 하는 리스트, 서버에 무슨색 점이지 구별할 필요가 있음
        self.difference=set()#갱신을 했으면 differ을 비워줌
        return paper,l#new points, 현재 자기가 갱신된 길이 리턴
    def updatePoints(self,points):
        for player_code,point in points:
            self.player_points[player_code].append(point)
    def draw(self):
        for idx,points_set in enumerate(self.player_points):
            self.drawPoints(points_set,pc[idx])
class ChatBox:
    def __init__(self,dm, x, y, w, h, text=''):
        self.dm=dm
        self.chatting=None
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.font=pygame.font.SysFont(FONT_NAME,10)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def event(self,event):
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:#엔터시
                    self.dm.scene.player.chat=self.text#플레이어의 chat을 갱신
                    self.text = ''#쓰는 상자 비우기
                elif event.key == pygame.K_BACKSPACE:#백스페이스시
                    self.text = self.text[:-1]#하나씩 지우기
                else:
                    self.text += event.unicode#한글변환은 추후에
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        #채팅 박스 크기 조절
        self.chatting=self.dm.scene.chatting
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        if len(self.chatting)>=1:
            self.cng=list(map(lambda x:self.font.render(x[1],True,pc[x[0]]),self.chatting))
            x=len(self.cng)-12 if len(self.cng)>11 else 0
            for idx, i in enumerate(range(x,len(self.cng))):
                self.dm.screen.blit(self.cng[i],(self.rect.x+5,50+20*idx))
        self.dm.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(self.dm.screen, self.color, self.rect, 2)

class Canvas(pygame.sprite.Sprite):
    def __init__(self,dm,image,x=0,y=0):
        self.rect=image.get_rect()
        self.rect.center=(x,y)
        self.image=image
        self.dm=dm
    def draw(self):
        self.dm.screen.blit(self.image,self.rect.center)
class RoomPacket:
    def __init__(self):
        self.code=None
        self.total_p_num=None#전체 인원수
        self.total_m_num=None#전체 마피아 수
        self.m_num=None#현재 마피아수
        self.p_num=None#현재 사람 수
        self.player_code=None#플레이어 unique code
        self.players=None#플레이어 객체들
        self.canvas=None
        self.paper=[]#종이 리스트
        self.chatting=[]#채팅 리스트
        self.m_idx=[]#마피아 플레이어 index
        self.master=None#방장
        self.reset_flag=False#브로드 캐스트 여부
        self.start_flag=False
        self.voting=False#투표 활성화
        self.word=None#제시어
        self.victory=False#누가 승리했는지
        self.end_flag=False#게임 종료
        self.who_catched=None#누가 잡았는지 알려주는 거
class Room:
    room_code=[True for i in range(ROOM_NUM)]#room assign
    def __init__(self,total_p_num):
        self.master=None
        self.canvas_catched=None#잡은 사람 player_code가 들어감
        self.code=self.get_code()
        self.total_p_num=total_p_num#전체 인원수
        self.total_m_num=total_p_num//4#전체 마피아 수
        self.m_num=0#현재 마피아수
        self.p_num=1#현재 사람 수
        self.player_code=[True for i in range(self.total_p_num)]#플레이어 unique code
        self.player_code[0]=False
        self.players=[PlayerPacket()]*self.total_p_num#플레이어 객체들
        for idx,i in enumerate(self.players):
            i.center=playerLocation[idx]
        self.paper=[]#종이 리스트
        self.chatting=[]#채팅 리스트
        self.m_idx=[]#마피아 플레이어 index
        self.reset_flag=False#broadcasting 상황인지 = 방을 리셋하라 시작하라 message받았는지
        self.reseted=[False]*self.total_p_num#player가 브로드 캐스트를 해야 하는지 여부
        self.started=[False]*self.total_p_num
        self.master=None#방장
        self.room_lock=allocate_lock()
        self.start_flag=False#게임 시작 했는지 여부
        self.drawed=[False]*self.total_p_num
        self.voted=[False]*self.total_p_num
        self.vote_content=['']*self.total_p_num
        self.voting=False#투표 활성화
        self.words=[]#제시어들
        self.word=None#제시어
        self.victory=False#False면 마피아 승리, True면 시민승리
        self.ended=[False]*self.total_p_num#끝나는 flag
        self.end_flag=False
        with open('./animal.txt',encoding='UTF8') as f:
            for line in f:
                if line!='\n':
                    self.words.append(line)
        self.m_idx=[]#마피아 idx
    def ending(self):
        #self.room_lock.acquire()
        self.canvas_catched=None#잡은 사람 player_code가 들어감
        self.paper=[]#종이 리스트
        self.m_idx=[]#마피아 플레이어 index
        self.reset_flag=False#broadcasting 상황인지 = 방을 리셋하라 시작하라 message받았는지
        self.reseted=[False]*8#player가 브로드 캐스트를 해야 하는지 여부
        self.started=[False]*8
        self.vote_content=['']*self.total_p_num
        self.word=None#제시어
        self.m_idx=[]#마피아 idx
        #self.room_lock.acquire()

    def getWord(self):
        return list(map(lambda x:x.strip(),self.words))[random.randint(0,len(self.words)-1)]
    def getPacket(self,playerPacket=None):
        room_packet=RoomPacket()
        room_packet.code=self.code
        room_packet.total_p_num=self.total_p_num
        room_packet.total_m_num=self.total_m_num
        room_packet.m_num=self.m_num
        room_packet.p_num=self.p_num
        room_packet.player_code=self.player_code
        room_packet.players=self.players
        room_packet.chatting=self.chatting# 채팅 리스트 형태(player_code, str chat)
        room_packet.m_idx=self.m_idx#마피아 idx
        room_packet.master=self.master#방장
        room_packet.victory=self.victory#default false(마피아 승리)
        room_packet.end_flag=self.end_flag
        room_packet.who_catched=self.canvas_catched
        self.room_lock.acquire()
        if playerPacket!=None:#playerPacket 파라미터가 들어왔으면 , 메뉴 화면에선 playerpacekt이아님!!
            if self.end_flag:#종료 flag라면
                self.ended[playerPacket.code]=True#보낼꺼니 true
                if False not in [x for idx,x in enumerate(self.ended) if not self.player_code[idx]]:#전부다 종료했다고 오면
                    self.end_flag=False
                    self.ended=[False]*self.total_p_num
            elif self.start_flag:
                room_packet.start_flag=True#시작한다고 or 게임중
                if playerPacket.code not in self.m_idx:#마피아가 아니면
                    room_packet.word=self.word#제시어를 보냄
                room_packet.voting=self.voting
                if not self.started[playerPacket.code]:#만약 시작한다고 알리지 않은 플레이어는
                    self.started[playerPacket.code]=True#이번에 보낼꺼니까
            elif not self.start_flag and self.reset_flag and self.reseted[playerPacket.code] and self.canvas_catched==None:#reset 상황이고 만약 자기가 브로드 캐스팅필요조건이 True면
                room_packet.reset_flag=True
                self.reseted[playerPacket.code]=False
                self.reset_flag=self.check_broadcasted(self.reseted)#브로드캐스트가 전부 되었다면 상황 종료
            if not self.reset_flag and playerPacket.total_len!=-1:#player가 갱신할 paper 선들이 있으면
                room_packet.paper=self.paper[playerPacket.total_len:]
        self.room_lock.release()
        return room_packet
    def check_broadcasted(self,broadcast,c=False):
        t=c
        for idx,b in enumerate(broadcast):
            if not self.player_code[idx] and not t:#할당된 아이디면
                c=b or c#하나라도 브로드 캐스트 실행해야 하는(True) 플레이어가 있으면 c=True가 됨
            elif not self.player_code[idx] and not t:#할당된 아이디면
                pass
        return c
    def add_player(self):
        self.room_lock.acquire()
        for idx,can in enumerate(self.player_code):
            if can:
                self.player_code[idx]=False
                self.p_num+=1
                self.room_lock.release()
                return idx
        self.room_lock.release()
    def remove_player(self,player):
        self.room_lock.acquire()
        if self.canvas_catched==player.code:
            self.canvas_catched=None
        self.player_code[player.code]=True
        self.p_num-=1
        self.room_lock.release()

    def update(self,player_packet):
        self.room_lock.acquire()
        self.players[player_packet.code]=player_packet#플레이어 패킷 갱신
        if player_packet.paper!=None and player_packet.canvas_catched:
            if len(player_packet.paper)>0:
                #print(f'[put]player{player_packet.code} {player_packet.paper}')
                self.paper+=player_packet.paper
        if self.voting:
            if player_packet.voting!=None:
                print(f'player{player_packet.code} voted \'{player_packet.voting}\'')
                if player_packet.code in self.m_idx:
                    print(f'self.word : {self.word}, word : {player_packet.voting}')
            if player_packet.voting is not None:
                self.voted[player_packet.code]=True#투표 여부
                self.vote_content[player_packet.code]=player_packet.voting#투표 내용 저장
                #print(f'content : {self.vote_content}',end='\n')
                #print(f'voted : {self.voted}',end='\n')
                if False not in [x for idx,x in enumerate(self.voted) if not self.player_code[idx]]:
                    #모두가 투표 했다면
                    self.voting=False#투표 종료
                    agree=True#마피아 한명이라도 걸리면 끝남.
                    for content in [self.vote_content[idx] for idx,x in enumerate(self.player_code) if (not x and idx not in self.m_idx)]:
                        agree*=str(content) in [str(i) for i in self.m_idx]#만장일치로 마피아를 찾는 변수
                    if not self.end_flag:#투표 종료 후 아무도 종료 flag를 set하지 않았다면
                        if (player_packet.code in self.m_idx and player_packet.voting==self.word):#마피아가 제시어를 맞추면
                            self.start_flag=False
                            self.victory=False#마피아 승리
                            print('마피아 승리')
                        elif agree:#만장일치로 마피아를 찾았다면
                            self.start_flag=False
                            self.victory=True#시민 승리
                            print('시민 승리')
                        if not self.start_flag:#게임 종료가 되었다면
                            self.ending()
                            self.end_flag=True
                    self.voted=[False]*self.total_p_num
                    self.drawed=[False]*self.total_p_num
        if player_packet.chat!='':#채팅을 쳤다면
            self.chatting.append((player_packet.code,player_packet.chat))
        self.room_lock.release()

    def start_room(self,c,net):#게임 시작과 종료까지 실행되는 함수 return은 자기가 나올때 방에 남은 사람
        while True:
            player_packet=net.recv(c)#playerPacket을 받음(paper, chat 주석임 현재)
            if not player_packet:
                break
            if player_packet.roomout_flag:#방 나가기 클릭시
                self.remove_player(player_packet)#플레이어 제거
                self.room_lock.acquire()
                self.canvas_catched=None
                self.room_lock.release()
                return self.p_num#자신 나가고 나머지 인원 수 반환
            elif player_packet.canvas_catched:#캔버스 근처에서 잡는 시도
                if (self.canvas_catched!=None and self.canvas_catched!=player_packet.code) or self.drawed[player_packet.code]:#잡은 사람이 있고 그게 자기가 아니면 or 자기가 그렸었다면
                    net.send(False,c)
                    continue
                elif self.canvas_catched==None and not self.drawed[player_packet.code]:#잡은사람이 없고 그린적이 없다면
                    net.send(True,c)
                    self.room_lock.acquire()
                    self.canvas_catched=player_packet.code#self.canvas_catched에 잡은 사람 player code 저장
                    self.room_lock.release()
                    #print(f'[catched]player{player_packet.code} canvas')
                    continue 
            elif not player_packet.canvas_catched and self.canvas_catched==player_packet.code:#놓는 시도 그게 자기라면
                self.room_lock.acquire()
                self.canvas_catched=None#잡은사람 없애기
                self.drawed[player_packet.code]=True
                if (False not in [x for idx,x in enumerate(self.drawed) if not self.player_code[idx]]):#all people drawed
                    if self.start_flag:#게임중이라면
                        self.voting=True
                    else:
                        self.drawed=[False]*self.total_p_num
                self.room_lock.release()
                #print(f'[droped]player{player_packet.code} canvas')
                continue
            elif player_packet.reset_room and self.canvas_catched==None and not self.start_flag:#player로 부터 reset_room flag를 받았다면, canvas를 아무도 잡고 있지 않다면
                self.room_lock.acquire()
                self.paper=[]
                if not self.reset_flag:#broadcasted flag
                    self.reset_flag=True#리셋 상황 시작
                    self.reseted=[True]*self.total_p_num#브로드 캐스팅 필요 여부
                    self.drawed=[False]*self.total_p_num#그릴 수 있는 권한 초기화
                self.room_lock.release()
            elif player_packet.start_room and not self.start_flag and not self.end_flag:#게임 시작을 눌렀으면
                self.room_lock.acquire()
                self.paper=[]
                l=[i for i in range(self.total_p_num) if not self.player_code[i]]#할당된 id code만 뽑음
                self.m_idx=random.sample(l,self.total_m_num)#마피아 뽑기
                self.word=self.getWord()
                self.canvas_catched=None
                self.start_flag=True
                self.drawed=[False]*self.total_p_num#그릴 수 있는 권한 초기화
                self.room_lock.release()
            self.update(player_packet)
            packet=self.getPacket(player_packet)
            net.send(packet,c)
    def get_code(self):
        for idx,can in enumerate(Room.room_code):
            if can:
                Room.room_code[idx]=False
                return idx
        return -1
    def release_code(self):
        Room.room_code[self.code]=True
class User(pygame.sprite.Sprite):
    def __init__(self,dm,player_code):
        self.dm=dm
        self.playerPacket=PlayerPacket()
        self.color=playerColor[player_code]
        self.dir=dir+self.color
        self.image=pygame.image.load(self.dir+PLAYER_DIR)
        self.rect=self.image.get_rect()
        self.rect.center=playerLocation[player_code]
        self.playerPacket.center=self.rect.center
        self.walkLRImages=list(map(lambda filename:pygame.image.load(self.dir+PLAYER_WALK_LR_DIR+str(filename)+'.png'),
        [filenum for filenum in range(8)]))
        self.walkUImages=list(map(lambda filename:pygame.image.load(self.dir+PLAYER_WALK_U_DIR+str(filename)+'.png'),
        [filenum for filenum in range(4)]))
        self.walkDImages=list(map(lambda filename:pygame.image.load(self.dir+PLAYER_WALK_D_DIR+str(filename)+'.png'),
        [filenum for filenum in range(4)]))
        self.hitImages=list(map(lambda filename:pygame.image.load(self.dir+PLAYER_HIT_DIR+str(filename)+'.png'),
        [filenum for filenum in range(4)]))
    def modify(self,playerpacket):
        self.playerPacket=playerpacket
    def draw(self):
        if self.playerPacket.state==1:
            self.dm.screen.blit(pygame.transform.flip(self.walkLRImages[self.playerPacket.frame],True,False),self.playerPacket.center)
        elif self.playerPacket.state==2:
            self.dm.screen.blit(self.walkLRImages[self.playerPacket.frame],self.playerPacket.center)
        elif self.playerPacket.state==3:
            self.dm.screen.blit(self.walkUImages[self.playerPacket.frame],self.playerPacket.center)
        elif self.playerPacket.state==4:
            self.dm.screen.blit(self.walkDImages[self.playerPacket.frame],self.playerPacket.center)
        elif self.playerPacket.state==0:
            self.dm.screen.blit(self.image,self.playerPacket.center)
        elif self.playerPacket.state==5:
            self.dm.screen.blit(self.hitImages[self.playerPacket.frame],self.playerPacket.center)
        elif self.playerPacket.state==6:
            self.dm.screen.blit(pygame.transform.flip(self.hitImages[self.playerPacket.frame],True,False),self.playerPacket.center)

class PlayerPacket:
    def __init__(self):
        self.code=None#player code
        self.center=None#플레이어 위치
        self.state=0#플레이어 행동 종류
        self.frame=0#플레이어 행동 frame
        self.chat=""#플레이어가 친 채팅
        self.paper=None#변경되는 내용만 담김
        self.roomout_flag=False#플레이어 방 나가기 flag
        self.canvas_catched=False#canvas 시도 여부
        self.total_len=None#갱신된 paper class의 playerPoints 길이
        self.master=False#마스터 여부
        self.reset_room=False#종이 초기화 flag
        self.start_room=False#게임 시작
        self.voting=None#false
    def reset_player(self):#플레이어 위치, 상태등 다 초기화
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self,dm,player_code,cursor_rect,canvas_rect):
        self.code=player_code
        self.paper=set()
        self.roomout_flag=False#방 나가기 flag
        self.chat=""
        self.state=0
        self.frame=0
        self.dm=dm
        self.color=playerColor[self.code]
        self.dir=dir+self.color
        self.image=pygame.image.load(self.dir+PLAYER_DIR)
        self.rect = self.image.get_rect()
        self.rect.center=playerLocation[self.code]
        self.cursor_rect=cursor_rect
        self.cursor_rect.center=self.rect.centerx+22,self.rect.centery-8,
        self.canvas_rect=canvas_rect
        self.voting=None
        ###event 제어 변수
        self.left=False
        self.right=False
        self.up=False
        self.down=False
        self.key_a=False
        self.during_key_a=False
        self.checkRecentRight=True#최근에 오른쪽인지 왼쪽인지
        self.direction=False        
        self.walkCountLR=0
        self.walkCountUD=0
        self.hitCount=0
        self.hitLastTime=0
        self.pre_keys=None
        self.canvas_catched=False#canvas를 d키를 눌러 잡으면 활성
        #게임 제어 변수
        self.master=False
        self.reset_room=False
        self.start_room=False
        ##이미지 리스트
        self.walkLRImages=list(map(lambda filename:pygame.image.load(self.dir+PLAYER_WALK_LR_DIR+str(filename)+'.png'),
        [filenum for filenum in range(8)]))
        self.walkUImages=list(map(lambda filename:pygame.image.load(self.dir+PLAYER_WALK_U_DIR+str(filename)+'.png'),
        [filenum for filenum in range(4)]))       
        self.walkDImages=list(map(lambda filename:pygame.image.load(self.dir+PLAYER_WALK_D_DIR+str(filename)+'.png'),
        [filenum for filenum in range(4)]))       
        self.hitImages=list(map(lambda filename:pygame.image.load(self.dir+PLAYER_HIT_DIR+str(filename)+'.png'),
        [filenum for filenum in range(4)]))
    def getPacket(self):
        packet=PlayerPacket()
        packet.code=self.code#player code
        packet.center=self.rect.center#플레이어 위치
        packet.state=self.state#플레이어 행동 종류
        packet.frame=self.frame#플레이어 행동 frame
        packet.roomout_flag=self.roomout_flag
        packet.chat=self.chat#플레이어가 친 채팅
        packet.canvas_catched=self.canvas_catched
        packet.paper,packet.total_len=self.dm.scene.paper.getNewPoints()#자신이 새로 등록한 점 추가
        packet.master=self.master
        packet.reset_room=self.reset_room
        self.reset_room=False#flag 전송하고 다시 false
        packet.start_room=self.start_room
        self.start_room=False
        packet.voting=self.voting
        if self.voting!='':#투표결과를 서버에 보냈으면 비움
            self.voting=None
        return packet
    def modifyId(self,code):
        self.code=code
        self.color=playerColor[self.code]
        self.dir=dir+self.color
        self.image=pygame.image.load(self.dir+PLAYER_DIR)
        self.rect.center=playerLocation[self.code]
    def reset(self):
        self.rect.center=tuple(self.dm.playersLocation[self.code-1])
    def Stand(self):
        self.key_a=False
        self.right=False
        self.left=False
        self.up=False
        self.down=False
        self.walkCountUD=0
        self.walkCountLR=0
    def Up(self):
        self.rect.centery-=PLAYER_V
        self.cursor_rect.centery=self.rect.centery-8
        if self.canvas_catched:
            self.canvas_rect.centery-=PLAYER_V
        self.key_a=False
        self.up=True
        self.down=False
        self.right=False
        self.left=False    
    def Down(self):
        self.rect.centery+=PLAYER_V
        self.cursor_rect.centery=self.rect.centery-8
        if self.canvas_catched:
            self.canvas_rect.centery+=PLAYER_V
        self.key_a=False
        self.down=True
        self.up=False
        self.right=False
        self.left=False
    def Left(self):
        self.rect.centerx-=PLAYER_V
        self.cursor_rect.centerx=self.rect.centerx+22
        if self.canvas_catched:
            self.canvas_rect.centerx-=PLAYER_V
        self.key_a=False
        self.up=False
        self.down=False
        self.left=True
        self.right=False
        self.direction=False        
    def Right(self):
        self.rect.centerx+=PLAYER_V
        self.cursor_rect.centerx=self.rect.centerx+22
        if self.canvas_catched:
            self.canvas_rect.centerx+=PLAYER_V
        self.key_a=False
        self.up=False
        self.down=False
        self.right=True
        self.left=False
        self.direction=True
    def event(self):
        keys=pygame.key.get_pressed()
        if self.pre_keys== None:
            self.pre_keys=keys
        if pygame.time.get_ticks()-self.dm.scene.player.hitLastTime>200 and self.dm.scene.player.key_a:
                self.dm.scene.player.key_a=False
                self.dm.scene.player.hitLastTime=0
                self.dm.scene.player.hitCount=0
        elif self.dm.scene.player.key_a:
            self.dm.scene.player.hitCount+=1
        else:
            if keys[pygame.K_a] and not self.dm.scene.player.key_a:#a키 실행중이 아니고 지금 눌렀다면
                self.dm.scene.player.hitLastTime=pygame.time.get_ticks()#cool체크
                self.dm.scene.player.key_a=True
                self.dm.scene.player.down=False
                self.dm.scene.hitSound[random.randint(0,len(self.dm.scene.hitSound)-1)].play()
                self.dm.scene.player.up=False
                self.dm.scene.player.right=False
                self.dm.scene.player.left=False
            elif not self.pre_keys[pygame.K_d] and keys[pygame.K_d] and self.canvas_rect.colliderect(self.rect):
                if self.canvas_catched==False:
                    self.canvas_catched=True
                    self.dm.net.send(self.getPacket(),self.dm.net.s)
                    can=self.dm.net.recv(self.dm.net.s)
                    if not can:
                        self.canvas_catched=False
            elif keys[pygame.K_LEFT]:
                self.dm.scene.player.Left()
            elif keys[pygame.K_RIGHT]:
                self.dm.scene.player.Right()
            elif keys[pygame.K_UP]:
                self.dm.scene.player.Up()
            elif keys[pygame.K_DOWN]:
                self.dm.scene.player.Down()
            else:
                self.dm.scene.player.Stand()
        self.pre_keys=keys
    def update(self):
        self.chat=''
    def draw(self):
        if self.walkCountLR>WALK_LR_UPA*(8-1):
            self.walkCountLR=0
        if self.walkCountUD>WALK_UD_UPA*(4-1):
            self.walkCountUD=0
        if self.hitCount>HIT_UPA*(4-1):
            self.hitCount=0
        if not self.key_a:
            if self.left:
                self.dm.screen.blit(pygame.transform.flip(self.walkLRImages[self.walkCountLR//WALK_LR_UPA],True,False),(self.rect.centerx,self.rect.centery))
                self.state=1
                self.frame=self.walkCountLR//WALK_LR_UPA
                self.walkCountLR+=1
            elif self.right:
                self.dm.screen.blit(self.walkLRImages[self.walkCountLR//WALK_LR_UPA],(self.rect.centerx,self.rect.centery))
                self.state=2
                self.frame=self.walkCountLR//WALK_LR_UPA
                self.walkCountLR+=1
            elif self.up:
                self.dm.screen.blit(self.walkUImages[self.walkCountUD//WALK_UD_UPA],(self.rect.centerx,self.rect.centery))
                self.state=3
                self.frame=self.walkCountUD//WALK_UD_UPA
                self.walkCountUD+=1
            elif self.down:
                self.dm.screen.blit(self.walkDImages[self.walkCountUD//WALK_UD_UPA],(self.rect.centerx,self.rect.centery))
                self.state=4
                self.frame=self.walkCountUD//WALK_UD_UPA
                self.walkCountUD+=1
            else:
                self.state=0
                self.frame=0
                self.dm.screen.blit(self.image,(self.rect.centerx,self.rect.centery))
        elif self.key_a:
            if self.direction:
                self.state=5
                self.hitCount//HIT_UPA
                self.frame=self.hitCount//HIT_UPA
                self.dm.screen.blit(self.hitImages[self.hitCount//HIT_UPA],(self.rect.centerx,self.rect.centery))
            else:
                self.state=6
                self.hitCount//HIT_UPA
                self.frame=self.hitCount//HIT_UPA
                self.dm.screen.blit(pygame.transform.flip(self.hitImages[self.hitCount//HIT_UPA],True,False),(self.rect.centerx,self.rect.centery))
                self.hitCount+=1
