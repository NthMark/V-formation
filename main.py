from math import sin, cos, atan2, radians, degrees
from random import randint
import pygame as pg
from pygame.math import Vector2
from pygame_screen_record.ScreenRecorder import ScreenRecorder
FLLSCRN = False          # True for Fullscreen, or False for Window
BIRDZ = 6           # How many birds to spawn, too many may slow fps
WRAP = False            # False avoids edges, True wraps to other side
FISH = False            # True to turn birds into fish
SPEED = 150             # Movement speed
WIDTH = 1200            # Window Width (1200)
HEIGHT = 800            # Window Height (800)
BGCOLOR = (0, 0, 0)     # Background color in RGB
FPS = 60                # 30-90
SHOWFPS = False         # frame rate debug


class Bird(pg.sprite.Sprite):

    def __init__(self, grid, drawSurf, isFish=False, isLead=False):  
        super().__init__()
        self.grid = grid
        self.drawSurf = drawSurf
        self.isLead=isLead
        self.image = pg.Surface((15, 15)).convert()
        self.image.set_colorkey(0)
        self.color = pg.Color(0)  
        self.color.hsva = (50, 90, 100) 
        if isLead:
            self.color.hsva=(0,100,100)
        pg.draw.polygon(self.image, self.color, ((7,0), (13,14), (7,11), (1,14), (7,0)))
        self.bSize = 22 if isFish else 17
        self.orig_image = pg.transform.rotate(self.image.copy(), -90)
        self.dir = pg.Vector2(1, 0)  # sets up forward direction
        maxW, maxH = self.drawSurf.get_size()
        self.index,self.parent=self.grid.getparent(self,isLead)
        print("Parent: {}".format(self.parent))
        self.rect = self.image.get_rect(center=self.grid.getcurrentbird(maxW,maxH,isLead))
        self.pos = pg.Vector2(self.rect.center)
        print("Current node:{}".format(self.pos))
        self.vec=Vector2()
        self.vel = pg.math.Vector2(0, 0)
        self.speed = 2
        self.angle=0
        self.tDistance=0
    def getvirtualpoint(self,parent):
        if parent.isLead:
            if self.index==2:
                self.vec.from_polar((self.grid.getdistance(),parent.angle+225))
                # print("real point: {}".format(self.parent.rect.center))
                # print("virtual point: {}".format(self.vec+pg.Vector2(parent.rect.center)))
                # print("--------------")
                return self.vec+pg.Vector2(parent.rect.center)
            elif self.index==3:
                self.vec.from_polar((self.grid.getdistance(),parent.angle+135))
                # print("real point: {}".format(self.parent.rect.center))
                # print("virtual point: {}".format(self.vec+pg.Vector2(parent.rect.center)))
                # print("--------------")
                return self.vec+pg.Vector2(parent.rect.center)
        else:
            if self.index%2==0:
                print("real point: {}".format(self.parent.rect.center))
                print("virtual point: {}".format(self.vec+pg.Vector2(parent.rect.center)))
                print("--------------")
                self.vec.from_polar((self.grid.getdistance(),parent.angle+225))
                return self.vec+pg.Vector2(parent.rect.center)
            else:
                self.vec.from_polar((self.grid.getdistance(),parent.angle+135))
                return self.vec+pg.Vector2(parent.rect.center)
    def update(self, dt, speed, ejWrap=False):
        if self.isLead:
            self.rotate(self.isLead)
            if not self.tDistance < self.bSize:
                self.pos += self.vel
            self.rect.center = self.pos
        else:
            self.rotate(self.isLead)
            if not self.tDistance < self.bSize:
                self.pos += self.vel
            self.rect.center = self.pos
    def rotate(self,isLead):
        if isLead:
            self.tDistance, self.angle = (pg.mouse.get_pos()-self.pos).as_polar()
            self.vel.from_polar((self.speed, self.angle))
            self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.tDistance, self.angle = (self.getvirtualpoint(self.parent)-self.pos).as_polar()
            self.vel.from_polar((self.speed, self.angle))
            self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
            if self.tDistance < self.bSize*2 :
                self.image = pg.transform.rotozoom(self.orig_image, -self.parent.angle, 1)
            self.rect = self.image.get_rect(center=self.rect.center)


class BirdGrid(): 

    def __init__(self):
        self.grid_size = 100
        self.dict = {}
        self.appear=[]
        self.distance=100
        self.angle=45
        self.parent=None
        self.birds=[]
    def getdistance(self):
        return self.distance
    def getangle(self):
        return self.angle
    def getparent(self,bird,isLead):
        if isLead:
            self.birds.append(bird)
            return (1,None)
        else:
            if len(self.birds)==1 or len(self.birds)==2 :
                self.birds.append(bird)
                return (len(self.birds),self.birds[0])
            else:
                self.birds.append(bird)
                return (len(self.birds),self.birds[len(self.birds)-3])
    def getparentbird(self,isLead):
        if isLead:
            self.bird
            return None
        else:
            if len(self.appear)==1 or len(self.appear)==2 :
                return self.appear[0]
            else:
                return self.appear[len(self.appear)-2]
    def getcurrentbird(self,maxW,maxH,isLead):
        if isLead:
            self.appear.append((maxW//2,maxH//2))
            return (maxW//2,maxH//2)
        else:
            basebird=self.getparentbird(isLead)
            dx=abs(sin(radians(self.angle))*self.distance)
            dy=abs(cos(radians(self.angle))*self.distance)
            tempy=basebird[1]+dy
            if len(self.appear)%2==1:
                tempx=basebird[0]-dx
            else:
                tempx=basebird[0]+dx
            self.appear.append((tempx,tempy))
            return (tempx,tempy)

def main():
    pg.init()  # prepare window
    pg.display.set_caption("V-formation")
    try: pg.display.set_icon(pg.image.load("bird.png"))
    except: print("Note: bird.png icon not found, skipping..")
    # setup fullscreen or window mode
    if FLLSCRN:
        currentRez = (pg.display.Info().current_w, pg.display.Info().current_h)
        screen = pg.display.set_mode(currentRez, pg.SCALED | pg.NOFRAME | pg.FULLSCREEN, vsync=1)
        pg.mouse.set_visible(False)
    else: screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE | pg.SCALED, vsync=1)

    birdTracker = BirdGrid()
    nbirds = pg.sprite.Group()
    # # spawns desired # of birdz
    nbirds.add(Bird(birdTracker, screen, FISH,True))
    for _ in range(BIRDZ) : nbirds.add(Bird(birdTracker, screen, FISH))

    if SHOWFPS : font = pg.font.Font(None, 30)
    clock = pg.time.Clock()
    # recorder = ScreenRecorder(60) # Pass your desired fps
    # recorder.start_rec() # Start recording
    # # main loop
    try:
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT or e.type == pg.KEYDOWN and (e.key == pg.K_ESCAPE or e.key == pg.K_q or e.key==pg.K_SPACE):
                    return

            dt = clock.tick(FPS) / 1000
            screen.fill(BGCOLOR)
            nbirds.update(dt, SPEED, WRAP)
            nbirds.draw(screen)
            # if true, displays the fps in the upper left corner, for debugging
            if SHOWFPS : screen.blit(font.render(str(int(clock.get_fps())), True, [0,200,0]), (8, 8))

            pg.display.update()
    finally:
        # recorder.stop_rec().get_single_recording().save(("v-formation","mp4"))
        pg.quit()
if __name__ == '__main__':
    
    main()  
    
