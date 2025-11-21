import pygame
import math
import sys

import random

pygame.init()
screenWidth = 800
screenHeight = 800
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("PlanetSim")

#fps display
clock = pygame.time.Clock()
def displayFPS(screen, fontSize):
    font = pygame.font.SysFont(None, fontSize)
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Player():
    def __init__(self, t_radius, pos):
        self.pos = pos
        self.t_radius = t_radius

        self.vel = (0, 0)

        self.gravity = (0, 0.5)
        
        self.gunForce = 15
    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), self.pos, self.t_radius)

    def physicsUpdate(self):

        #apply gravity accelaration
        self.vel = (self.vel[0], self.vel[1] + self.gravity[1])

        #apply velocity
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])

        #bounce of edges
        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])
            self.vel = (self.vel[0] * -1, self.vel[1])
        if self.pos[0] > screenWidth:
            self.pos = (screenWidth, self.pos[1])
            self.vel = (self.vel[0] * -1, self.vel[1])

    def shoot(self):
        #do knockback

        #get to mouse direction
        mPos = pygame.mouse.get_pos()
        vecToMouse = (mPos[0] - self.pos[0], mPos[1] - self.pos[1])
        oppositeVec = (vecToMouse[0] * -1, vecToMouse[1] * -1)
        mag = math.sqrt(oppositeVec[0] ** 2 + oppositeVec[1] ** 2)
        normalizedVec = (oppositeVec[0] / mag, oppositeVec[1] / mag)

        #apply opposite force by gunForce
        self.vel = (normalizedVec[0] * self.gunForce, normalizedVec[1] * self.gunForce)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

plyr = Player(10, (400, 200))

running = True
while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                plyr.shoot()
        

    screen.fill((0, 0, 0))

    plyr.physicsUpdate()
    plyr.draw()

    displayFPS(screen, 20)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()