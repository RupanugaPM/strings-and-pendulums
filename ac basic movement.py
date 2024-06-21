import pygame,sys,random,copy,math,time

pygame.init()
mainclock=pygame.time.Clock()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")

char_x = 0#y position of gmaincharacter
char_y = 0#x position of gmaincharacter
width = 40#height of display
height = 60#width of display
vel = 3#velocity of the gcharacters
particles=[]#particles which change with time
saved_particles=[]#particles are saved when e is pressed
mouseloc=[0,0]#where mouse is located when e is pressed

def cartesian_to_polar(xo,yo,x,y):
    #distance from xo,yo
    rx=x-xo
    ry=y-yo
    r=(rx**2+ry**2)**(1/2)
    #there is still division by zero error left but that should not happen... that happened so i used try and except below
    try:
        #1 quadrant
        if (x-xo)>=0 and (y-yo)>=0:   
            theta = math.atan(ry/rx)
        #2 and 3 quadrant    
        if ((x-xo) <= 0 and (y-yo) >= 0) or ((x-xo) <= 0 and (y-yo) <= 0):
            theta = math.atan(ry/rx)+math.pi
        #4 quadrant
        if (x-xo) >= 0 and (y-yo) <= 0:
            theta = math.atan(ry/rx)+math.pi*2
    except:
        if rx==0:
            theta=math.pi/2
        else:
            theta=0            
    return r,theta  

def polar_to_cartesian(xo,yo,r,theta):
    #very simple this one 🙂
    return math.cos(theta)*r+xo,math.sin(theta)*r+yo

def get_angle(a, b, c):
    #gets angle between 3 points
    ang = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
    return ang 

start_time = time.time()

while True:

    actual_fps = 1/((time.time()-start_time+0.01))
    start_time = time.time()
    pygame.display.set_caption("First Game"+str(int(actual_fps)))
    vel = 3*(60/actual_fps)

    win.fill((0, 0, 0))
    a=pygame.mouse.get_pressed()[0]
    angle_btw_mn_c_mo = get_angle(mouseloc, (char_x+width/2, char_y+height/2), pygame.mouse.get_pos())#gives the angle between old mouse position,character center and new mouse position with respect to character center

    if a == 1:  # pygame.mouse.get_pressed() is used to check which mouse button is pressed
        particles.append([[char_x+width/2, char_y+height/2], [(pygame.mouse.get_pos()[0]-(char_x+width/2))/50,(pygame.mouse.get_pos()[1]-(char_y+height/2))/50], 12])# particle is appended if mouse is clicked which has center(x,y),velocity(x,y),radius of circle/particle

    iteration_constant=0#will be used when we pop during iteration
    nparticles=[]
    for particle in particles:
        #updating postion
        particle[0][0] += (60/actual_fps)*particle[1][0]  # updating velocity x
        particle[0][1] += (60/actual_fps)*particle[1][1]  # updating velocity y
        #changing radius
        particle[2] -= 0.2
        #drawing color
        pygame.draw.circle(win, (255,0,255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        #removing particle
        if particle[2] > 0:#remove particle if velocity
            nparticles.append(particle)
        iteration_constant += 1
    particles=nparticles
    
    #quiting function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #checking key presses     
    keys = pygame.key.get_pressed()
    #moving charecter
    if keys[pygame.K_a]:
        char_x -= vel
        mouseloc[0] -= vel
        for sparticle in saved_particles:
            sparticle[0][0] -= vel
    if keys[pygame.K_d]:
        char_x += vel
        mouseloc[0] += vel
        for sparticle in saved_particles:
            sparticle[0][0] += vel
    if keys[pygame.K_w]:
        char_y -= vel
        mouseloc[1] -= vel
        for sparticle in saved_particles:
            sparticle[0][1] -= vel
    if keys[pygame.K_s]:
        char_y+=vel
        mouseloc[1]+=vel
        for sparticle in saved_particles:
            sparticle[0][1]+=vel
    #appending and hence saving particle if e is pressed    
    if keys[pygame.K_e]:
        ##you should update this if you press e other wise saved particle will return to its original position
        if len(saved_particles)!=0:
            for sparticle in saved_particles:
                r_theta_sparticle = list(cartesian_to_polar(char_x+width/2, char_y+height/2,sparticle[0][0],sparticle[0][1]))# polar coordinates of sparticle
                r_theta_sparticle[1]+=angle_btw_mn_c_mo#updating theta of polar coordinates to make it move with mouse
                sparticle[0][0] = polar_to_cartesian(char_x+width/2, char_y+height/2, r_theta_sparticle[0],r_theta_sparticle[1])[0]#updated x coordinate of sparticle
                sparticle[0][1] = polar_to_cartesian(char_x+width/2, char_y+height/2, r_theta_sparticle[0],r_theta_sparticle[1])[1]#updated y coordinate of sparticle
        ##end of updation       
        for particle in particles:
            a = [particle[0], particle[2]]
            saved_particles.append(a)
        #deep copying the list     
        saved_particles = copy.deepcopy(saved_particles)
        mouseloc=list(pygame.mouse.get_pos())
    #removing particles from saved particles    
    if keys[pygame.K_q]:
        saved_particles =[]
    
    for sparticle in saved_particles:
        
        r_theta_sparticle = list(cartesian_to_polar(char_x+width/2, char_y+height/2,sparticle[0][0],sparticle[0][1]))# polar coordinates of sparticle
           
        r_theta_sparticle[1]+=angle_btw_mn_c_mo#updating theta of polar coordinates to make it move with mouse
        up_x_sparticle = polar_to_cartesian(char_x+width/2, char_y+height/2, r_theta_sparticle[0],r_theta_sparticle[1])[0]#updated x coordinate of particle
        up_y_sparticle = polar_to_cartesian(char_x+width/2, char_y+height/2, r_theta_sparticle[0],r_theta_sparticle[1])[1]#updated y coordinate of particle
        pygame.draw.circle(win, (255,0,255), [int(up_x_sparticle), int(up_y_sparticle)], int(sparticle[1]))
    print(len(saved_particles))
    
    #drawing character
    pygame.draw.rect(win, (255,0,0), (int(char_x), int(char_y), width, height))   
    pygame.display.update() 
    mainclock.tick(60)
