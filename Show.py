import pygame
import random
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def show(the_map):
    pygame.init()
    pygame.display.set_mode((600,600), DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1, 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    angle = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 0)
        
        glPushMatrix()
        glTranslatef(0.0,0.0, -5)
        glRotated(30, 1, 0, 0)
        glRotated(angle, 0, 1, 0)
        
        glTranslatef(-1, 0, -1)
        glScalef(2/the_map.side, 1, 2/the_map.side)
        glColor3f(0.1, 0.9, 0.1)
        glBegin(GL_QUADS)
        for i in range(the_map.side-1):
            for j in range(the_map.side-1):
                glVertex3f(i  , the_map.map[i][j]    , j)
                glVertex3f(i+1, the_map.map[i+1][j]  , j)
                glVertex3f(i+1, the_map.map[i+1][j+1], j+1)
                glVertex3f(i  , the_map.map[i][j+1]  , j+1)
        glEnd()
        
        glPopMatrix()
        
        pygame.display.flip()
        angle += .5
        pygame.time.wait(10)
    pygame.quit()

