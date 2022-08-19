import pygame
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

HEIGHT = 720
WIDTH = 1280
GSIZEX = 2000
GSIZEY = 2000
lockcamera = False
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pydew Valley Prototype")

def convcoord(x,y):
    global camera
    return (x+camera[0],y+camera[1])

def getdrawablearea():
    global camera
    result = []
    for x in range(camera[0]-WIDTH/2,camera[0]+WIDTH/2):
        for y in range(camera[1]-HEIGHT/2,camera[1]+HEIGHT/2):
            result.append((x,y))
    return result

objlist = []

class DrawObject:
    def __init__(self,gx,gy,sx,sy,colour,speed=0,nocollide = False,useplayer=False):
        self.gx = gx
        self.gy = gy
        self.prev_pos = [(0,0)]
        self.size_x = sx
        self.size_y = sy
        self.colour = colour
        self.surf = pygame.Surface((sx,sy))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect()
        self.speed = speed
        self.nc = nocollide
        self.up = useplayer
        objlist.append(self)
    def get_syx(self,camera):
        return (camera[0] - self.gx, camera[1] - self.gy)
    def getcoords(self):
        result = []
        for x in range(self.size_x):
            for y in range(self.size_y):
                result.append((x,y))
        return result
    def update(self,pressed_keys):
        self.rect = pygame.Rect(self.get_syx(camera)[0],self.get_syx(camera)[1],self.size_x,self.size_y)
        
        if self.up:
            if self.gx > -(GSIZEX / 2) and self.gx < GSIZEX / 2  and self.gy > -(GSIZEY / 2) and self.gy < GSIZEY/2:

                if pressed_keys[pygame.K_UP]:
                    self.gy += self.speed
                if pressed_keys[pygame.K_DOWN]:
                    self.gy -= self.speed
                if pressed_keys[pygame.K_RIGHT]:
                    self.gx -= self.speed
                if pressed_keys[pygame.K_LEFT]:
                    self.gx += self.speed
            else:
                self.gx = 0
                self.gy = 0
            
            for obj in objlist:
                if obj is not self:
                    if obj.nc:
                        if self.rect.colliderect(obj.rect):
                            
                            print("Collision detected")
                            print(self.prev_pos)
                            for pos in self.prev_pos:
                                print(pos)
                                self.gx,self.gy = pos
                                if self.rect.colliderect(pygame.Rect(obj.get_syx(camera)[0],obj.get_syx(camera)[1],obj.size_x,obj.size_y)):
                                    continue
                                else:
                                    break

            self.prev_pos.insert(0, (self.gx,self.gy))
            self.prev_pos = self.prev_pos[0:4] #Limiting size so it doesn't eat up all the memory
        
    def draw(self,win):
        global camera
        win.blit(self.surf,self.get_syx(camera))


def draw_text(surface,text,size,color,x,y):
    font = pygame.font.SysFont("Colsolas",size)
    label = font.render(text,False,color)
    surface.blit(label,(x,y))
DrawObject((GSIZEX/2),(GSIZEY/2),GSIZEX,GSIZEY,(0,0,0),0,False,False)
DrawObject(5,5,35,35,(0,255,0),0,False,False)
player = DrawObject(0,0,25,25,(255,255,255),1,True,True)

DrawObject(-23,-438,100,100,(64,64,64),0,True,False)

def game2local(x,y):
    return (camera[0] + x,camera[1] + y)

def local2game(x,y):
    return (camera[0] - x, camera[1] - y)

def get_blocksq():
    m = pygame.mouse.get_pos()
    gamepos = local2game(m[0],m[1])
    blockpos = ((i//50)+1 for i in gamepos)
    blockpos = list((i*50 for i in blockpos))
    return game2local(-blockpos[0],-blockpos[1]) #WHY ARE MY AXIS INVERTED

run = True
clock = pygame.time.Clock()
tck = 0
while run:
    tck += 1
    win.fill((255,0,0))
    if not lockcamera:
        camera = (player.gx + WIDTH/2,player.gy + HEIGHT/2)
        #print(camera)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
                
    pressed_keys = pygame.key.get_pressed()
    for obj in objlist:
        obj.update(pressed_keys)
        obj.draw(win)
    x = get_blocksq()
    sq = pygame.Surface((50,50))
    sq.fill((255,255,255))
    sq.set_alpha(128)
    win.blit(sq,pygame.Rect(x[0],x[1],50,50)) #Selected block
        
    draw_text(win,f"X: {str(int(player.gx))} | Y: {str(int(player.gy))} | FPS: {str(round(clock.get_fps()))} | MX: {str(pygame.mouse.get_pos()[0])} | MY: {str(pygame.mouse.get_pos()[1])}",28,(255,255,255),0,0)
    pygame.display.update()
    clock.tick(1000)