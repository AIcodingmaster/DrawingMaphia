import os
import pygame
#charater state 패킷
"""
(playerID: x,y,color/ 행동ID:행동frame
"""
#행동 ID
"""
0: 가만히
1:왼쪽이동
2:오른쪽이동
3:위로이동
4:아래로이동
5:오른쪽떄리기
6:왼쪽 떄리기
"""

#Player color
playerColor={0:"red",1:"green",2:"orange",3:"pink",4:"purple",5:"blue",6:"white",7:"yellow"}
pc={0:(255,0,0),1:(0,255,0),2:(255,94,0),3:(255,0,188),4:(85,0,255),5:(0,0,255),6:(255,255,255),7:(239,255,0)}



#User id(자리배치)
"""
        1
    8        5    
4               2
    7        6
        3
"""

#Base prop
TITLE = "Drawing Mafia"
WIDTH = 600
HEIGHT = 350
FPS = 20

#Font
FONT_NAME = 'malgungothic'

#define colors
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
BROWN = (111, 109, 81)
BACKGROUND_COLOR=(9,8,16)
#Image
CANVAS_DIR="./imgs/canvas.png"#1

dir="./imgs/"
PLAYER_DIR="/char.png"#1
PLAYER_WALK_LR_DIR="/playerWalking/"#8
PLAYER_WALK_U_DIR="/playerWalkingUp/"#4
PLAYER_WALK_D_DIR="/playerWalkingDown/"#4
PLAYER_HIT_DIR="/playerHit/"#4
MAIN_BACKGROUND=dir+"main/background.png"

#sound
soundDir="./music/"
MAIN_SOUND=soundDir+'main.wav'
CLICK_SOUND=soundDir+'click.wav'
GAME_SOUND=soundDir+'game.wav'

#Player Init Location (12시 부터 순서 방향),canvas Location, Player 속도
H3=HEIGHT/3
H12=HEIGHT/12
W3=WIDTH/3
W12=WIDTH/12
playerLocation=[(W3+W12*2,H3),(W3*2,H3+H12*2),(W3+W12*2,H3*2),(W3+W12*0,H3+H12*2),
(W3+W12*3,H3+H12),(W3+W12*3,H3+H12*3),(W3+W12,H3+H12*3),(W3+W12,H3+H12)]#8인 위치 
canvasLocation=(WIDTH/2,HEIGHT/2)
PLAYER_V=5

#Action Cool & Update Num per Action frame
HIT_COOL=200
WALK_LR_UPA=3
WALK_UD_UPA=5
HIT_UPA=3