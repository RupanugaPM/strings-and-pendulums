import numpy as np
from scipy.linalg import solve
import pygame

class Pendulum:
    def __init__(self, n=5, thetas=None, theta_dots=None, g=-29.8, length=50):
        self.n = n
        self.thetas = np.full(n, 0.5 * np.pi) if thetas is None else np.array(thetas)
        self.theta_dots = np.zeros(n) if theta_dots is None else np.array(theta_dots)
        self.g = g
        self.length = length  # Length of each pendulum arm
        self.origin = (400, 100)  # Origin position for drawing

    def A(self, thetas):
        M = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row.append((self.n - max(i, j)) * np.cos(thetas[i] - thetas[j]))
            M.append(row)
        return np.array(M)

    def b(self, thetas, theta_dots):
        v = []
        for i in range(self.n):
            b_i = 0
            for j in range(self.n):
                b_i -= (self.n - max(i, j)) * np.sin(thetas[i] - thetas[j]) * theta_dots[j] ** 2
            b_i -= self.g * (self.n - i) * np.sin(thetas[i])
            v.append(b_i)
        return np.array(v)

    def f(self, thetas, theta_dots):
        A = self.A(thetas)
        b = self.b(thetas, theta_dots)
        theta_dot_dots = solve(A, b)
        return np.array([theta_dots, theta_dot_dots])

    def RK4(self, dt, thetas, theta_dots):
        k1 = self.f(thetas, theta_dots)
        k2 = self.f(thetas + 0.5 * dt * k1[0], theta_dots + 0.5 * dt * k1[1])
        k3 = self.f(thetas + 0.5 * dt * k2[0], theta_dots + 0.5 * dt * k2[1])
        k4 = self.f(thetas + dt * k3[0], theta_dots + dt * k3[1])
        
        theta_deltas = (dt / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        theta_dot_deltas = (dt / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        
        new_thetas = thetas + theta_deltas
        new_theta_dots = theta_dots + theta_dot_deltas
        
        return new_thetas, new_theta_dots

    def tick(self, dt):
        self.thetas, self.theta_dots = self.RK4(dt, self.thetas, self.theta_dots)

    @property
    def coordinates(self):
        x, y = 0, 0
        coords = []
        for theta in self.thetas:
            x += self.length * np.sin(theta)
            y += self.length * np.cos(theta)
            coords.append((self.origin[0] + x, self.origin[1] - y))  # Note the change here
        return coords

    def draw(self, screen):
        coords = self.coordinates
        for i, (x, y) in enumerate(coords):
            if i == 0:
                pygame.draw.line(screen, (0, 0, 0), self.origin, (x, y), 2)
            else:
                pygame.draw.line(screen, (0, 0, 0), coords[i-1], (x, y), 2)
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 5)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pendulum = Pendulum()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    pendulum.tick(0.01)
    pendulum.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
