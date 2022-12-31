import pygame
from pygame.locals import *
from OpenGL.GL import *
from loader import loadMap
from shared import Entity, Static

WINDOW_WIDTH, WINDOW_HEIGHT = 640, 640


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE|OPENGL|DOUBLEBUF)
pygame.display.set_caption("My Pygame Window")

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, 640, 640, 0, 0, 640)
glMatrixMode(GL_MODELVIEW)

map1 = loadMap("res/map1.png")
entities: list[Entity] = map1["entities"]
statics: list[Static] = map1["statics"]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1, 1, 1, 1)

    for entity in entities:
        entity.update(0.1, entities, statics)
    
    for static in statics:
        static.draw()
    
    for entity in entities:
        entity.draw()

    # Swap buffers and update the display
    pygame.display.flip()


pygame.quit()