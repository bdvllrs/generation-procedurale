import pygame
import random
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


def colorize(value, keys):
    if value in keys:
        return keys[value]
    start, end = 0, 1
    for k in keys:
        if start < k <= value:
            start = k
        elif value < k <= end:
            end = k
    Rs, Gs, Bs, As = keys[start]
    Re, Ge, Be, Ae = keys[end]
    pe = (value-start)/(end-start)
    ps = 1-pe
    return [Rs*ps+Re*pe, Gs*ps+Ge*pe, Bs*ps+Be*pe, As*ps+Ae*pe]

def show(the_map):
    # Initialisation
    pygame.init()
    pygame.display.set_mode((600,600), DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1, 0.1, 50.0)
    
    glMatrixMode(GL_MODELVIEW)
    glMaterialf(GL_FRONT_AND_BACK,GL_SHININESS,10.0)
    glLoadIdentity()

    # Echelle de couleurs
    palette = {0   : [0.2, 0.2, 0.2, 1],
               0.2 : [0.2, 0.2, 0.2, 1],
               0.3 : [0.2, 0.5, 0.2, 1],
               0.75: [0.5, 0.5, 0.5, 1],
               1   : [0.8, 0.8, 0.8, 1]}

    # Colorize chaque point
    print('Calcul des couleurs...')
    colorMap = [[colorize(the_map.map[i][j], palette) for j in range(the_map.side)] for i in range(the_map.side)]

    # Crée la display list
    print('Génération du rendu...')
    index = glGenLists(1)
    glNewList(index, GL_COMPILE)
    
    glBegin(GL_TRIANGLES)
    for i in range(the_map.side-1):
        for j in range(the_map.side-1):
            glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR,colorMap[i][j])
            glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE,colorMap[i][j])
            
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
    glBegin(GL_QUADS)
    glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR,[0.2, 0.2, 0.8, 0.5])
    glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE,[0.2, 0.2, 0.8, 0.5])
    glNormal3f(0, 1, 0)
    for i in range(the_map.side-1):
        for j in range(the_map.side-1):
            mean = (the_map.map[i][j]+the_map.map[i+1][j]+the_map.map[i][j+1]+the_map.map[i+1][j+1])/4
            if(mean <= 0.25):
                glVertex3f(i, 0.25, j)
                glVertex3f(i+1, 0.25, j)
                glVertex3f(i+1, 0.25, j+1)
                glVertex3f(i, 0.25, j+1)
    glEnd()
    glEndList()
    print('Rendu généré!')

    # Variables d'affichage
    angle = 0
    LRSpeed = 0
    UDSpeed = 0
    autoRotate = True
    zoomFactor = 1.
    orient = 30.

    # Boucle Principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    autoRotate = False
                    LRSpeed -= 1
                elif event.key == pygame.K_RIGHT:
                    autoRotate = False
                    LRSpeed += 1
                elif event.key == pygame.K_UP:
                    autoRotate = False
                    UDSpeed -= 1
                elif event.key == pygame.K_DOWN:
                    autoRotate = False
                    UDSpeed += 1
                elif event.key == pygame.K_RETURN:
                    if UDSpeed == 0 and LRSpeed == 0:
                        autoRotate = not autoRotate
                elif event.unicode == '+':
                    zoomFactor *= 1.1
                elif event.unicode == '-':
                    zoomFactor /= 1.1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    autoRotate = False
                    LRSpeed += 1
                elif event.key == pygame.K_RIGHT:
                    autoRotate = False
                    LRSpeed -= 1
                elif event.key == pygame.K_UP:
                    autoRotate = False
                    UDSpeed += 1
                elif event.key == pygame.K_DOWN:
                    autoRotate = False
                    UDSpeed -= 1
            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 0)
        
        glPushMatrix()
        glTranslatef(0.0,0.0, -5)
        glRotated(orient, 1, 0, 0)
        glRotated(angle, 0, 1, 0)
        
        glLightiv(GL_LIGHT0,GL_POSITION,[0, 5, 0, 0])

        glScalef(zoomFactor, zoomFactor, zoomFactor)
        glTranslatef(-1, 0, -1)
        glScalef(2/the_map.side, 1, 2/the_map.side)
        glColor3f(0.1, 0.1, 0.1)
        
        glCallList(index)
        glPopMatrix()
        
        pygame.display.flip()
        if autoRotate:
            angle += .2
        else:
            angle += 0.5*LRSpeed
            orient += 0.2*UDSpeed
        pygame.time.wait(10)
    glDeleteLists(index, 1)
    pygame.quit()

