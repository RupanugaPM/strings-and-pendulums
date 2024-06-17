import pygame, sys, random , time

width=800
height=800

clock = pygame.time.Clock()
pygame.init() # initiates pygame
pygame.display.set_caption('Caption')
WINDOW_SIZE = (width,height)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

vec2=pygame.math.Vector2
class Segments():
    def __init__(self,l,gravity=[0,0]):
        #l is list of points where (assumed that len(l)>=2)
        self.l=[vec2(i[0],i[1]) for i in l]
        self.gravity=vec2(gravity[0],gravity[1])
        self.speed=[vec2(0,0) for i in range(len(l)-1)]
        
    def update(self,pos):
        prev=vec2(pos[0],pos[1])
        if self.gravity.length():
            for i in range(len(self.l)-1):
                self.speed[i]+=self.gravity
                tmp=self.gravity.project(self.l[i]-self.l[i+1])
                self.speed[i]-=tmp
                self.l[i+1]=self.l[i]+self.speed[i]
        for i in range(len(self.l)-1):
            tmp=(self.l[i]-self.l[i+1]).length()
            tmp2=(self.l[i+1]-prev)
            tmp2.scale_to_length(tmp)
            self.l[i]=prev
            prev=prev+tmp2
        self.l[-1]=prev
    def addsegment(self, length,angle):
        x=self.l[-1]
        ex=vec2.from_polar([length,angle])
        self.speed.append(vec2(0, 0))
        self.l.append(vec2(x+ex))
    def show(self):
        if len(self.l)>=2:
            pygame.draw.lines(screen, (255, 255, 255), False, self.l)



class Starfield():
    def __init__(self):
        self.x=random.randint(-width//2,width//2)
        self.y=random.randint(-height//2,height//2)
        self.z=random.randint(width//2,width)
        self.sx=(self.x//self.z)*width
        self.sy=(self.y//self.z)*height
        self.radius=((width-self.z)/width)*8
        self.color=(255,255,255)
        self.speedz=3
        self.speedy=0
        self.speedx=0
        #self.accelertiony=1
    def update(self):
        if (self.z-self.speedz<=20)or ((width/2+self.sx+self.radius<=0) or (width/2+self.sx-self.radius>=height)) or ((height/2+self.sy+self.radius<=0) or (height/2+self.sy-self.radius>=height)):
            self.z=random.randint(width//2,width)
            self.x=random.randint(-width//2,width//2)
            self.y=random.randint(-height//2,height//2)
        self.z-=self.speedz
        if self.speedy<-10:
            self.speedy=10
        self.sx=(self.x/self.z)*(width/2)
        self.sy=(self.y/self.z)*(height/2)
        self.radius=((width-self.z)/width)*8
    def show(self):
        pygame.draw.circle(screen, self.color, [width/2+self.sx,height/2+ self.sy], self.radius)

#l=[Starfield() for i in range(int(100))]
tentacle=Segments([[400,400]]) 
for i in range(30):
    tentacle.addsegment(10,90)

while True: # game loop
    screen.fill((0,0,0))
    mx, my = pygame.mouse.get_pos()
    spd=pygame.mouse.get_pos()[0]/16

    # for i in range(len(l)):
    #     l[i].update()
    #     l[i].show()
    #     l[i].speedz=spd
    tentacle.update([mx, my])
    

    tentacle.show()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    # moving charecter
    # print(keys[pygame.K_a])
    if keys[pygame.K_a]:
        time.sleep(1)
    pygame.display.update()
    clock.tick(60)