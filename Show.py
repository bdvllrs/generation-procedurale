import pygame
import random
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def show(the_map):
    # Initialisation
    pygame.init()
    pygame.display.set_mode((600,600), DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1, 0.1, 50.0)
    
    glMatrixMode(GL_MODELVIEW)
    glMaterialiv(GL_FRONT_AND_BACK,GL_SPECULAR,[1, 1, 1, 1])
    glMateriali(GL_FRONT_AND_BACK,GL_SHININESS,100)
    glLightiv(GL_LIGHT0,GL_POSITION,[2, 5, 2, 1])
    glLoadIdentity()

    # Crée la display list

    index = glGenLists(1)
    glNewList(index, GL_COMPILE)
    
    glBegin(GL_TRIANGLES)
    for i in range(the_map.side-1):
        for j in range(the_map.side-1):
            v1 = the_map.map[i][j] - the_map.map[i+1][j]     # on x
            v2 = the_map.map[i+1][j] - the_map.map[i+1][j+1] # on y
            n = v1**2 + v2**2 + 1
            v1 /= n
            v2 /= n
            glNormal3f(-v1, 1/n, -v2)
            glVertex3f(i  , the_map.map[i][j]    , j)
            glVertex3f(i+1, the_map.map[i+1][j]  , j)
            glVertex3f(i+1, the_map.map[i+1][j+1], j+1)
            
            v1 = the_map.map[i][j+1] - the_map.map[i+1][j+1] # on x
            v2 = the_map.map[i][j] - the_map.map[i][j+1]     # on y
            n = v1**2 + v2**2 + 1
            v1 /= n
            v2 /= n
            glNormal3f(-v1, 1/n, -v2)
            glVertex3f(i+1, the_map.map[i+1][j+1], j+1)
            glVertex3f(i  , the_map.map[i][j+1]  , j+1)
            glVertex3f(i  , the_map.map[i][j]    , j)
    glEnd()
    glEndList()

    # Boucle Principale
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
        
        glCallList(index)
        glPopMatrix()
        
        pygame.display.flip()
        angle += .2
        pygame.time.wait(10)
    glDeleteLists(index, 1)
    pygame.quit()

