import pygame
from model import *
from setting import *
class  Main: 
    def __init__(self,DM): #변수, 게임 기본설정 초기화
        self.dm=DM
        self.background=pygame.image.load(MAIN_BACKGROUND)
        self.background_rect=self.background.get_rect(left=0,top=0)
        self.font=pygame.font.SysFont(FONT_NAME,20)
        self.fontItalic=pygame.font.SysFont(FONT_NAME,40,italic=True)
        self.title= self.fontItalic.render('Drawingmafia',True,WHITE)
        self.title_rect=self.title.get_rect(left=20,top=150)
        self.findRoom4= self.font.render('방 참가(4인)',True,WHITE)
        self.findRoom4_rect=self.findRoom4.get_rect(left=450,top=130)
        self.findRoom8= self.font.render('방 참가(8인)',True,WHITE)
        self.findRoom8_rect=self.findRoom8.get_rect(left=450,top=170)
        self.makeRoom4= self.font.render('방 생성(4인)',True,WHITE)
        self.makeRoom4_rect=self.makeRoom4.get_rect(left=450,top=210)
        self.makeRoom8= self.font.render('방 생성(8인)',True,WHITE)
        self.makeRoom8_rect=self.makeRoom8.get_rect(left=450,top=250)
        self.codeFindRoom= self.font.render('방 코드 참가',True,WHITE)
        self.codeFindRoom_rect=self.codeFindRoom.get_rect(left=450,top=290)
        pygame.mixer.music.load(MAIN_SOUND)
        self.clickSound=pygame.mixer.Sound(CLICK_SOUND)
        self.clickSound.set_volume(1.0)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()
    def stop(self):
        pygame.mixer.music.stop()
    def update(self):
        #메인화면 애니메이션 같은거 찾아보기
        pass
    def event(self):
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.mixer.music.stop()
                self.dm.dm_running=False
            elif self.findRoom4_rect.collidepoint(pygame.mouse.get_pos()):
                self.findRoom4=self.font.render('방 참가(4인)',True,YELLOW)
            elif self.findRoom8_rect.collidepoint(pygame.mouse.get_pos()):
                self.findRoom8=self.font.render('방 참가(8인)',True,YELLOW)
            elif self.makeRoom4_rect.collidepoint(pygame.mouse.get_pos()):
                self.makeRoom4=self.font.render('방 생성(4인)',True,YELLOW)
            elif self.makeRoom8_rect.collidepoint(pygame.mouse.get_pos()):
                self.makeRoom8=self.font.render('방 생성(8인)',True,YELLOW)
            elif self.codeFindRoom_rect.collidepoint(pygame.mouse.get_pos()):
                self.codeFindRoom=self.font.render('방 코드 참가',True,YELLOW)
            elif self.background_rect.collidepoint(pygame.mouse.get_pos()):#글자가 아닌 배경에 마우스가 있을 경우
                self.findRoom4=self.font.render('방 참가(4인)',True,WHITE)
                self.findRoom8=self.font.render('방 참가(8인)',True,WHITE)
                self.makeRoom4=self.font.render('방 생성(4인)',True,WHITE)
                self.makeRoom8=self.font.render('방 생성(8인)',True,WHITE)
                self.codeFindRoom=self.font.render('방 코드 참가',True,WHITE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.findRoom4_rect.collidepoint(event.pos):
                    self.dm.net.send("f4",self.dm.net.s)
                    player_code=self.dm.net.recv(self.dm.net.s)
                    room=self.dm.net.recv(self.dm.net.s)
                    self.dm.changeScene(Game(self.dm,room,player_code))
                    self.clickSound.play()
                elif self.findRoom8_rect.collidepoint(event.pos):
                    self.dm.net.send("f8",self.dm.net.s)
                    player_code=self.dm.net.recv(self.dm.net.s)
                    room=self.dm.net.recv(self.dm.net.s)
                    self.dm.changeScene(Game(self.dm,room,player_code))
                    self.clickSound.play()
                elif self.makeRoom4_rect.collidepoint(event.pos):
                    self.dm.net.send("m4",self.dm.net.s)
                    room=self.dm.net.recv(self.dm.net.s)
                    self.dm.changeScene(Game(self.dm,room,0))
                    self.clickSound.play()
                elif self.makeRoom8_rect.collidepoint(event.pos):
                    self.dm.net.send("m8",self.dm.net.s)
                    room=self.dm.net.recv(self.dm.net.s)
                    self.dm.changeScene(Game(self.dm,room,0))
                    self.clickSound.play()
                elif self.codeFindRoom_rect.collidepoint(event.pos):
                    #코드로 방찾기 추가 필요
                    self.clickSound.play()
    def draw(self): #화면에 그려주는 함수
        self.dm.screen.blit(self.background,self.background_rect)
        self.dm.screen.blit(self.title,self.title_rect)
        self.dm.screen.blit(self.findRoom4,self.findRoom4_rect)
        self.dm.screen.blit(self.findRoom8,self.findRoom8_rect)
        self.dm.screen.blit(self.makeRoom4,self.makeRoom4_rect)
        self.dm.screen.blit(self.makeRoom8,self.makeRoom8_rect)
        self.dm.screen.blit(self.codeFindRoom,self.codeFindRoom_rect)

class Game:
    def __init__(self,DM,room,player_code): #변수, 게임 기본설정 초기화
        self.mafia=False
        self.dm=DM
        self.room=room
        self.font=pygame.font.SysFont(FONT_NAME,10)
        self.fontItalic=pygame.font.SysFont(FONT_NAME,40,italic=True)
        self.roomfont=self.font.render(f'코드 : {self.room.code}',True,BLACK)
        self.roomfont_rect=self.roomfont.get_rect(left=WIDTH-100,top=18)  
        self.word=''
        self.mafiafont=self.font.render(f'마피아',True,RED)
        self.mafiafont_rect=self.mafiafont.get_rect(left=WIDTH//2-20,top=18)
        self.citizenfont=self.font.render(f'시민',True,BLUE)
        self.citizenfont_rect=self.citizenfont.get_rect(left=WIDTH//2-20,top=18)     
        self.wordfont=self.font.render(f'제시어 : {self.word}',True,BLACK)
        self.wordfont_rect=self.wordfont.get_rect(left=WIDTH//2-20,top=35)

        self.chatImage=pygame.image.load("./imgs/chat.png")
        self.chatImage_rect=self.chatImage.get_rect(left=18,top=18)
        self.cursor=pygame.image.load("./imgs/cursor.png")
        self.cursor_rect=self.chatImage.get_rect()
        self.outRoomImage=pygame.image.load("./imgs/roomout.png")
        self.outRoomImage_rect=self.outRoomImage.get_rect(left=WIDTH-50,top=18)
        
        self.resetImage=pygame.image.load("./imgs/reset.png")
        self.resetImage_rect=self.resetImage.get_rect(left=WIDTH-140,top=18)
        self.startImage=pygame.image.load("./imgs/start.png")
        self.startImage_rect=self.startImage.get_rect(left=WIDTH-180,top=18)

        self.canvasImage=pygame.image.load(CANVAS_DIR)
        self.canvas=Canvas(self.dm,self.canvasImage,WIDTH//2,HEIGHT//2)#중앙에 canvas 배치
        self.player=Player(self.dm,player_code,self.cursor_rect,self.canvas.rect)
        self.users=[None]*8
        #paper
        self.paper=Paper(self.dm)
        self.d_active=False#누른 상태
        self.last_pos=None#전 point를 저장

        #chatting active 버튼
        self.chatActive=False
        self.chatImage=pygame.image.load("./imgs/chat.png")
        self.chatImage_rect=self.chatImage.get_rect(left=18,top=18)
        #chatting
        self.font=pygame.font.SysFont(FONT_NAME,10)
        self.chat=ChatBox(self.dm,10,HEIGHT-40,140,24)
        self.chatting=None

        self.start_room=False
        self.gameSound=pygame.mixer.Sound(GAME_SOUND)
        self.gameStartSound=pygame.mixer.Sound('./music/game_start.wav')
        self.mafia_win_sound=pygame.mixer.Sound('./music/mafia_win.wav')
        self.citizen_win_sound=pygame.mixer.Sound('./music/mafia_lose.wav')



        self.voting=False#투표 활성화
        self.voted=False#투표했는지
        self.inputbox=InputBox(WIDTH//2-80,HEIGHT-70,180,36,self.dm)
        self.font2=pygame.font.SysFont(FONT_NAME,15)
        self.votefont=self.font2.render(f'투표 : ',True,BLACK)
        self.mafiavotefont=self.font2.render(f'제시어: ',True,BLACK)
        self.mafiavotefont_rect=self.mafiavotefont.get_rect(left=WIDTH//2-137,top=HEIGHT-63)  
        self.votefont_rect=self.votefont.get_rect(left=WIDTH//2-130,top=HEIGHT-63)  

        self.color_image=pygame.image.load('./imgs/4color.png') if self.room.total_p_num==4 else pygame.image.load('./imgs/8color.png')

        self.votedfont=self.font.render(f'투표 완료, 다른 플레이어를 기다리세요',True,BLACK)
        self.votedfont_rect=self.votedfont.get_rect(left=WIDTH//2-100,top=80)  
        self.hitSound=[]
        for i in range(3):
            self.hitSound.append(pygame.mixer.Sound(soundDir+f'attack{i}.wav'))
    def stop(self):
        pygame.mixer.stop()
    def setStart(self):
        self.start_room=True
        self.gameSound.play(-1)
        self.gameStartSound.play()
        self.d_active=False#누른 상태
        self.last_pos=None#전 point를 저장
        self.dm.scene.player.canvas_catched=False
    def ending(self):
        self.canvas.rect.center=(WIDTH//2,HEIGHT//2)
        self.mafia=False
        self.d_active=False#누른 상태
        self.paper.resetPaper()#paper초기화
        self.chatActive=False
        self.voting=False#투표 활성화
        self.voted=False#투표했는지
        self.word=''#단어 초기화
        self.player.rect.center=playerLocation[self.player.code]
        self.gameSound.stop()
        self.start_room=False
        if self.room.victory:
            self.citizen_win_sound.play()
            print('citizen victory')
        else:
            self.mafia_win_sound.play()
            print('mafia victory')
    def draw(self): #화면에 그려주는 함수
        self.dm.screen.fill((255,255,255))
        self.dm.screen.blit(self.chatImage,self.chatImage_rect)
        if not self.start_room:
            self.dm.screen.blit(self.roomfont,self.roomfont_rect)
            self.dm.screen.blit(self.outRoomImage,self.outRoomImage_rect)
            self.dm.screen.blit(self.startImage,self.startImage_rect)
            self.dm.screen.blit(self.resetImage,self.resetImage_rect)
        self.canvas.draw()
        if self.chatActive:
            self.chat.draw()
        if self.player.canvas_catched or self.room.who_catched is not None:#누군가 잡았거나 내가 잡았다면
            self.dm.screen.blit(self.cursor,self.cursor_rect)
        for user in self.users:
            if user!=None:
                user.draw()
        self.player.draw()
        self.paper.draw()
        if self.voting:
            if not self.voted:
                self.inputbox.draw()
                if not self.mafia:
                    self.dm.screen.blit(self.votefont,self.votefont_rect)
                    self.dm.screen.blit(self.color_image,(WIDTH//2-130,HEIGHT-90))
                else:
                    self.dm.screen.blit(self.mafiavotefont,self.mafiavotefont_rect)
            else:
                self.dm.screen.blit(self.votedfont,self.votedfont_rect)
        if self.start_room:#게임중인 방에서만 그리는 것
            if self.mafia:
                self.dm.screen.blit(self.mafiafont,self.mafiafont_rect)
            else:#시민이면
                self.dm.screen.blit(self.wordfont,self.wordfont_rect)
                self.dm.screen.blit(self.citizenfont,self.citizenfont_rect)
    def event(self):
        if self.voting and not self.voted:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.mixer.music.stop()
                    self.player.roomout_flag=True
                    self.dm.net.send(self.player.getPacket(),self.dm.net.s)
                    self.dm.game_running=False
                    exit()
                self.inputbox.handle_event(event)
        elif self.voting and self.voted:
            pass
        else:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.mixer.music.stop()
                    self.player.roomout_flag=True
                    self.dm.net.send(self.player.getPacket(),self.dm.net.s)
                    self.dm.game_running=False
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.d_active=True#d_active를 킴
                    if self.outRoomImage_rect.collidepoint(event.pos):
                        self.player.roomout_flag=True
                        self.dm.net.send(self.player.getPacket(),self.dm.net.s)#방을 나간다고 서버에 알려주고
                        self.dm.changeScene(Main(self.dm))#main scene으로 돌아감
                        return
                    elif self.startImage_rect.collidepoint(event.pos) and not self.player.start_room:
                        self.player.start_room=True
                    elif self.resetImage_rect.collidepoint(event.pos) and not self.player.reset_room:
                        self.player.reset_room=True
                    elif self.chatImage_rect.collidepoint(event.pos):
                        self.chatActive=not self.chatActive
                        if not self.chatActive:
                            self.chat.active=False
                    elif self.chat.rect.collidepoint(event.pos):
                        if self.chatActive:
                            self.chat.active=True
                    elif not self.chat.rect.collidepoint(event.pos) or not self.chatImage_rect.collidepoint(event.pos):
                        self.chatActive=False
                        self.chat.active=False
                elif event.type==pygame.MOUSEBUTTONUP:
                    if self.player.canvas_catched==True:#one touch drawing with player
                        self.player.canvas_catched=False
                        self.dm.net.send(self.player.getPacket(),self.dm.net.s)
                    self.d_active=False
                    self.last_pos=None
                self.chat.event(event)#pygame.event.get을 다시 부르기 불가, event인자 받아서 처리
            if not self.chat.active:#채팅 활성화시 캐릭터 이동 및 다른 행동 불가
                self.player.event()
            self.paper.event()#paper event함수
    def update(self):
        self.cursor_rect.center=(self.canvas.rect.centerx+22,self.canvas.rect.centery-8)
        self.dm.net.send(self.player.getPacket(),self.dm.net.s)
        self.room=self.dm.net.recv(self.dm.net.s)
        #방 패킷으로 넘어온 정보 저장
        self.voting=self.room.voting
        if not self.voting:
            self.voted=False
        if self.room.end_flag and self.start_room:#난 게임중인데 서버에서 끝났다고 면
            self.ending()#엔딩 함수
        if self.voting and not self.voted:#투표 상황이고 투표를 안했다면
            self.inputbox.update()
        elif self.room.start_flag and not self.start_room and not self.room.end_flag:#서버에서 게임 시작 버튼이 눌렸다고 오면
            self.dm.scene.paper.resetPaper()#paper을 비움
            self.setStart()#게임 세팅 초기화
            if self.player.code in self.room.m_idx:
                self.mafia=True
            if not self.mafia:
                self.word=self.room.word
                self.wordfont=self.font.render(f'제시어 : {self.word}',True,BLACK)#갱신
        elif self.room.reset_flag:
            self.dm.scene.paper.resetPaper()#paper을 비움
        for idx,can in enumerate(self.room.player_code):
            if not can and idx!=self.player.code:#할당된 아이디고 내 id가 아니라면(다른)
                if self.users[idx]==None:#새로 들어온 유저면
                    self.users[idx]=User(self.dm,idx)
                else:#원래 있던 유저면
                    self.users[idx].modify(self.room.players[idx])
            elif can:#나간 유저라면 삭제
                self.users[idx]=None
        self.chatting=self.room.chatting
        self.paper.updatePoints(self.room.paper)
        self.player.update()
        self.chat.update()
                
