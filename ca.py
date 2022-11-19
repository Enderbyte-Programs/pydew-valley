import math

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

win = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Game v0.0.1-dev5")
win.fill((0,0,255))
def draw_text(surface,text,size,color,x,y):
    font = pygame.font.SysFont("Colsolas",size)
    label = font.render(text,False,color)
    surface.blit(label,(x,y))
draw_text(win,"Enderbyte Programs",64,(255,0,255),100,100)
draw_text(win,"Generating Terrain",28,(255,255,255),0,0)
pygame.display.update()
grid = [[1 for i in range(GSIZEX//50)] for j in range(GSIZEY//50)]
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

            self.prev_pos.insert(0, (round(self.gx),round(self.gy)))
            self.prev_pos = self.prev_pos[0:4] #Limiting size so it doesn't eat up all the memory
        
    def draw(self,win):
        global camera
        win.blit(self.surf,self.get_syx(camera))



def checkspawn(coord):
    x,y = coord
    lx = x - GBLOCKX / 2
    ly = y - GBLOCKY / 2
    if (lx > 5 or lx < -5) or (ly > 5 or ly < -5):
        return True
    else:
        return False

def fixfps():
    fps = round(clock.get_fps())
    if fps > 150:
        return 1
    elif fps < 151 and fps > 75:
        return 2
    elif fps < 76 and fps > 49:
        return 3
    elif fps < 50 and fps > 25:
        return 4
    elif fps < 26 and fps > 15:
        return 8
    else:
        return 10



#Drawing terrain
for i in range(int(round(math.sqrt(GBLOCKX*GBLOCKY))/2)):# Averageing list then /2 to get 20
    ry = random.randint(0,len(grid)-1)
    rx = random.randint(0,len(grid[ry])-1)
    if checkspawn((rx,ry)):
        try:
            grid[rx][ry] = 3 #Assumes rectangle | Drawing rock
        except:
            pass
    else:
        print("Bad rng for rock " + str(rx) +  ","+str(ry))

for i in range(int(round(math.sqrt(GBLOCKX*GBLOCKY))/2/4)):
    spt = (random.randint(0,len(grid)-1),random.randint(0,len(grid[0])-1))
    if checkspawn(spt):
        for y in range(spt[0]-random.randint(1,3),spt[0]+random.randint(0,3)):
            for x in range(spt[1]-random.randint(1,3),spt[1]+random.randint(0,3)):
                try:
                    grid[y][x] = 6
                except:
                    print("Bad position for water",x,y)
    else:
        print("Bad rng for water",spt)

for i in range(int(round(math.sqrt(GBLOCKX*GBLOCKY))/2/4)):
    spt = (random.randint(0,len(grid)-1),random.randint(0,len(grid[0])-1))
    if checkspawn(spt):
        for y in range(spt[0]-random.randint(1,3),spt[0]+random.randint(0,3)):
            for x in range(spt[1]-random.randint(1,3),spt[1]+random.randint(0,3)):
                try:
                    grid[y][x] = 4
                except:
                    print("Bad position for forest",x,y)
    else:
        print("Bad RNG for forest",spt)

for i in range(int(round(math.sqrt(GBLOCKX*GBLOCKY))/2//3)):
    spt = (random.randint(0,len(grid)-1),random.randint(0,len(grid[0])-1))
    if checkspawn(spt):
        for y in range(spt[0]-random.randint(1,3),spt[0]+random.randint(0,3)):
            for x in range(spt[1]-random.randint(1,3),spt[1]+random.randint(0,3)):
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
            inc += 1
            if not x == 0:               

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
                elif x == 7:
                    if li is not None:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(0,0,0),0,False,False,li+inc)
                    else:
                        DrawObject((_xi)*50,(_yi)*50,50,50,(0,0,0),0,False,False,None)
                
        _xi = -(GSIZEX/2//50)
GRIDSTART = len(objlist)
GRIDEND = GRIDSTART + (GSIZEX//50)*(GSIZEY//50)
drawgrid()
blockids = ["oom","grass","dirt","rock","dense_forest","light_forest","water","void"]
toolids = ["pointer","shovel","Pickaxe","Seed","Sponge","Bucket","Axe"]
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
def get_player_block():
    #print(int((player.gy//50)+(GBLOCKY/2)))
    #print(int((player.gx//50)+(GBLOCKX/2)))
    try:
        return grid[int((player.gy//50)+(GBLOCKY/2))][int((player.gx//50)+(GBLOCKX/2))]
    except:
        return 0
run = True
cim = None
TOOL = 0

clock = pygame.time.Clock()
tck = 0
speedmultiplier = 1
gametime = 0 # 10000 ticks good maybe?
while run:
    if not TOOL == 0:
        if TOOL != 0:
            pygame.mouse.set_visible(False)
            cim = pygame.Surface((20,20)) #Replace with image at M1
            if TOOL == 1:
                cim.fill((128,128,128))
            elif TOOL == 2:
                cim.fill((255,0,0))
            elif TOOL == 3:
                cim.fill((0,128,0))
            elif TOOL == 4:
                cim.fill((255,255,0))
            elif TOOL == 5:
                cim.fill((0,0,255))
            elif TOOL == 6:
                cim.fill((64,64,64))
    if tck > 9 and tck // 10 == tck /10:
        player.speed = fixfps()
    tck += 1
    gametime += 1
    drawrect = pygame.Rect((0,0,WIDTH,HEIGHT))
        
    if gametime > 10000 and gametime < 20000:
        
        nightsurf = pygame.Surface((WIDTH,HEIGHT))
        nightsurf.fill((0,0,0))
        if gametime > 10000 and gametime < 12000:
            nightsurf.set_alpha(round((gametime-10000)/10))
        elif gametime > 12000 and gametime < 18001:
            nightsurf.set_alpha(200)
        elif gametime > 18000 and gametime < 20001:
            nightsurf.set_alpha(round((-(gametime-20000))/10))
    elif gametime > 20000:
        gametime = 0#resetting to 0 when day is over
        
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
            elif event.key == pygame.K_2:
                TOOL = 2
            elif event.key == pygame.K_3:
                TOOL = 3
            elif event.key == pygame.K_4:
                TOOL = 4
            elif event.key == pygame.K_5:
                TOOL = 5
            elif event.key == pygame.K_6:
                TOOL = 6
            elif event.key == pygame.K_0:
                TOOL = 0
                cim = None
                pygame.mouse.set_visible(True)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            oldgrid = grid
            mp = pygame.mouse.get_pos()
            gp = local2game(mp[0],mp[1])
            bp = (int(gp[0]//50 + GBLOCKX/2),int(gp[1]//50 + GBLOCKY/2))
            print(bp)
            # Checking tool
            if TOOL == 1:
                try:
                    if grid[bp[1]][bp[0]] == 1:
                        grid[bp[1]][bp[0]] = 2
                except IndexError:
                    pass
            elif TOOL == 2:
                try:
                    if grid[bp[1]][bp[0]] == 3:
                        grid[bp[1]][bp[0]] = 2
                except IndexError:
                    pass
            elif TOOL == 3:
                try:
                    if grid[bp[1]][bp[0]] == 2:
                        grid[bp[1]][bp[0]] = 1
                    elif grid[bp[1]][bp[0]] == 1:
                        grid[bp[1]][bp[0]] = 5
                    elif grid[bp[1]][bp[0]] == 5:
                        grid[bp[1]][bp[0]] = 4
                except IndexError:
                    pass
            elif TOOL == 4:
                try:
                    if grid[bp[1]][bp[0]] == 6:
                        a = random.choice([2,2,2,2,2,2,2,2,2,3])#10% chance
                        grid[bp[1]][bp[0]] = a
                except IndexError:
                    pass

            elif TOOL == 5:
                try:
                    if grid[bp[1]][bp[0]] != 6:
                        grid[bp[1]][bp[0]] = 6
                except IndexError:
                    pass

            elif TOOL == 6:
                try:
                    if grid[bp[1]][bp[0]] == 4:
                        grid[bp[1]][bp[0]] = 5
                    elif grid[bp[1]][bp[0]] == 5:
                        grid[bp[1]][bp[0]] = 1
                except IndexError:
                    pass


            del objlist[GRIDSTART:GRIDEND]
            drawgrid(GRIDSTART)
            #print(grid)
        elif event.type == pygame.VIDEORESIZE:
            win = pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)
            WIDTH = event.w
            HEIGHT = event.h
                
    pressed_keys = pygame.key.get_pressed()
    for obj in objlist:
        obj.update(pressed_keys)
        if drawrect.colliderect(obj.rect):
            obj.draw(win)
    x = get_blocksq()
    if gametime > 10000 and gametime < 20000:
        win.blit(nightsurf,drawrect)
    sq = pygame.Surface((50,50))
    sq.fill((255,255,255))
    sq.set_alpha(128)
    win.blit(sq,pygame.Rect(x[0],x[1],50,50)) #Selected block
    pblock = get_player_block()
   
    draw_text(win,f"X: {str(int(player.gx))} | Y: {str(int(player.gy))} | FPS: {str(round(clock.get_fps()))} | MX: {str(pygame.mouse.get_pos()[0])} | MY: {str(pygame.mouse.get_pos()[1])} | TM: {str(gametime)} | BLK: {blockids[pblock]} | TL: {toolids[TOOL]} | WXY: {(WIDTH,HEIGHT)}",28,(255,255,255),0,0)
    if cim is not None:
        win.blit(cim,pygame.mouse.get_pos())
    
    if pblock == 5 or pblock == 6:
        speedmultiplier = 0.75
        player.speed = player.speed*speedmultiplier
    elif pblock == 7:
        player.gx = 0
        player.gy = 0
    pygame.display.update()
    clock.tick()