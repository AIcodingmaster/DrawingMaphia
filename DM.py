from scene import *
from setting import *
from network import Net
class DM:
    def __init__(self):
        self.dm_running=True#Drawing Maphia 시작
        self.main_running=True#메인 화면
        self.game_running=False#방 화면
        self.code_running=False
        self.net=Net()
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