from scene import *
from setting import *
from network import Net
'''
  File "c:\pythonprojects\DrawingMafia\network.py", line 30, in recv
    data=loads(data_b)
EOFError: Ran out of input
겜하는 도중 에러 -> 해결
마피아 word 비교 에러->해결
마피아 다 나가면 게임 종료->해결
다른 유저 공격소리추가->해결
방장 여부 ->해결
8인방 투표 에러-> 해결
방 코드로 들어가기 -> 해결
ending 다르게 해서 보여주기->?? 해야되나
'''



class DM:
    def __init__(self): 
        self.dm_running=True#Drawing Maphia 시작
        self.main_running=True#메인 화면
        self.game_running=False#방 화면
        self.code_running=False
        self.net=Net()
        #self.net.init_client(('15.165.162.81',5556))
        self.net.init_client(('localhost',5555))
        pygame.init()
        self.scene=Main(self)
        pygame.mixer.init() 
        pygame.display.set_caption(TITLE)
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock=pygame.time.Clock()
    def changeScene(self,newScene):
        self.scene.stop()
        self.scene=newScene
    def update(self):
        self.scene.update()
        pygame.display.update()
    def event(self):
        self.scene.event()
    def draw(self):
        self.screen.fill((255,255,255))
        self.scene.draw()
    def run(self):
        while self.dm_running:
            self.draw()
            self.event()
            self.update()
            pygame.display.update()
            self.clock.tick(30)
        pygame.quit()


dm=DM()
dm.run()    