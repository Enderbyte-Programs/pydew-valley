import pygame
import sys
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

HEIGHT = 720
WIDTH = 1280
GSIZEX = 2000
GSIZEY = 2000
GBLOCKX = GSIZEX // 50
GBLOCKY = GSIZEY // 50
lockcamera = False
grid = [[1 for i in range(GSIZEX//50)] for j in range(GSIZEY//50)]
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
    def __init__(self,gx,gy,sx,sy,colour,speed=0,nocollide = False,useplayer=False,lin = None):
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
        self.lin = None
        if lin is not None:
            self.lin = lin
            objlist.insert(lin,self)
        else:
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

#Drawing terrain
for i in range(20):
    ry = random.randint(0,len(grid)-1)
    rx = random.randint(0,len(grid[ry])-1)
    if (ry > 5 or ry < -5) or (rx> 5 or rx < -5):
        grid[rx][ry] = 3 #Assumes rectangle | Drawing rock
    else:
        print("Bad rng for rock " + str(rx) +  ","+str(ry))

for i in range(3):
    spt = (random.randint(0,len(grid)-1),random.randint(0,len(grid[0])-1))
    if (spt[0] > 5 or spt[0] < -5) or (spt[1] > 5 or spt[1] < -5):
        for y in range(spt[0]-2,spt[0]+2):
            for x in range(spt[1]-2,spt[1]+2):
                try:
                    grid[y][x] = 6
                except:
                    print("Bad position for water",x,y)
    else:
        print("Bad rng for water",spt)

for i in range(5):
    spt = (random.randint(0,len(grid)-1),random.randint(0,len(grid[0])-1))
    if (spt[0] > 5 or spt[0] < -5) or (spt[1] > 5 or spt[1] < -5):
        for y in range(spt[0]-2,spt[0]+2):
            for x in range(spt[1]-2,spt[1]+2):
                try:
                    grid[y][x] = 4
                except:
                    print("Bad position for forest",x,y)
    else:
        print("Bad RNG for forest",spt)

for i in range(8):
    spt = (random.randint(0,len(grid)-1),random.randint(0,len(grid[0])-1))
    if (spt[0] > 5 or spt[0] < -5) or (spt[1] > 5 or spt[1] < -5):
        for y in range(spt[0]-2,spt[0]+2):
            for x in range(spt[1]-2,spt[1]+2):
                try:
                    grid[y][x] = 5
                except:
                    print("Bad position for forest",x,y)
    else:
        print("Bad rng for forest",spt)
    
def drawgrid(li=None):
    inc = -1
    _xi = -(GSIZEX/2//50)
    _yi = -(GSIZEY/2//50)
    for y in grid:
        _yi += 1
        
        for x in y:
            _xi += 1
            if not x == 0:
                inc += 1
                indx = (_xi,_yi)
                if x == 1:
                    if li is not None:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(0,128,0),0,False,False,li+inc)
                    else:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(0,128,0),0,False,False,None)
                elif x == 2:
                    if li is not None:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(123,63,0),0,False,False,li+inc)
                    else:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(123,63,0),0,False,False,li)
                elif x == 3:
                    if li is not None:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(64,64,64),0,True,False,li+inc)
                    else:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(64,64,64),0,True,False,li)
                elif x == 4:
                    if li is not None:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(0,64,0),0,True,False,li+inc)
                    else:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(0,64,0),0,True,False,li)
                elif x == 5:
                    if li is not None:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(64,255,64),0,False,False,li+inc)
                    else:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(64,255,64),0,False,False,li)
                elif x == 6:
                    if li is not None:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(0,0,255),0,False,False,li+inc)
                    else:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(0,0,255),0,False,False,li)
        _xi = -(GSIZEX/2//50)
GRIDSTART = len(objlist)
GRIDEND = GRIDSTART + (GSIZEX//50)*(GSIZEY//50)
drawgrid()

DrawObject(5,5,35,35,(0,255,0),0,False,False)
player = DrawObject(0,0,25,25,(255,255,255),1,True,True)


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
cim = None
TOOL = 0
if not TOOL == 0:
    if TOOL == 1:
        pygame.mouse.set_visible(False)
        cim = pygame.Surface((20,20)) #Replace with image at M1
        cim.fill((128,128,128))
clock = pygame.time.Clock()
tck = 0
while run:
    tck += 1
    win.fill((0,0,0))
    if not lockcamera:
        camera = (player.gx + WIDTH/2,player.gy + HEIGHT/2)
        #print(camera)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_1:
                TOOL = 1
                pygame.mouse.set_visible(False)
                cim = pygame.Surface((20,20)) #Replace with image at M1
                cim.fill((128,128,128))
            elif event.key == pygame.K_0:
                TOOL = 0
                cim = None
                pygame.mouse.set_visible(True)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            gp = local2game(mp[0],mp[1])
            bp = (int(gp[0]//50 + GBLOCKX/2),int(gp[1]//50 + GBLOCKY/2))
            print(bp)
            # Checking tool
            if TOOL == 1:
                if grid[bp[1]][bp[0]] == 1:
                    grid[bp[1]][bp[0]] = 2

            del objlist[GRIDSTART:GRIDEND]
            drawgrid(GRIDSTART)
            #print(grid)
                
    pressed_keys = pygame.key.get_pressed()
    for obj in objlist:
        obj.update(pressed_keys)
        obj.draw(win)
    x = get_blocksq()
    sq = pygame.Surface((50,50))
    sq.fill((255,255,255))
    sq.set_alpha(128)
    win.blit(sq,pygame.Rect(x[0],x[1],50,50)) #Selected block
        
    draw_text(win,f"X: {str(int(player.gx))} | Y: {str(int(player.gy))} | FPS: {str(round(clock.get_fps()))} | MX: {str(pygame.mouse.get_pos()[0])} | MY: {str(pygame.mouse.get_pos()[1])} | TK: {str(tck)}",28,(255,255,255),0,0)
    if cim is not None:
        win.blit(cim,pygame.mouse.get_pos())
    pygame.display.update()
    clock.tick(1000)