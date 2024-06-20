import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Purple Rain')

Window_width = 700
Window_height = 700
WINDOW_SIZE = (Window_width, Window_height)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

rain_color = (152, 68, 158)

def map(x, x1, x2, y1, y2):
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

class Rain():
    def __init__(self):
        self.x = random.randint(5, 695)
        self.y = random.randint(-1500, -5)
        self.z = random.randint(0, 30)
        self.width = random.randint(1, 3)
        self.color = list(rain_color)
        self.speedy = map(self.z, 0, 30, 0.5, 2)
        self.length = map(self.z, 0, 30, 10, 20)
    
    def fall(self):
        self.y += self.speedy
        self.speedy += (0.025 * self.z) / 30
        if self.y >= 700:
            self.y = random.randint(-200, -100)
            self.speedy = random.uniform(0.5, 2)
    
    def display(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.length))

num_drops = 700
rainfall = [Rain() for _ in range(num_drops)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # Clear screen with black before drawing

    for drop in rainfall:
        drop.fall()
        drop.display()
    
    pygame.display.update()
    clock.tick(60)
