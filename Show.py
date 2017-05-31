import pygame
import random
import math
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
    pygame.display.set_mode((1366,728), DOUBLEBUF | OPENGL) #| pygame.FULLSCREEN)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1, 0.1, 50.0)
    #glOrtho(-2,2,-2,2,0,8)
    
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
            n = math.sqrt(v1**2 + v2**2 + 1)
            v1 /= n
            v2 /= n
            glNormal3f(-v1, 1/n, -v2)
            glVertex3f(i  , the_map.map[i][j]    , j)
            glVertex3f(i+1, the_map.map[i+1][j]  , j)
            glVertex3f(i+1, the_map.map[i+1][j+1], j+1)
            
            v1 = the_map.map[i][j+1] - the_map.map[i+1][j+1] # on x
            v2 = the_map.map[i][j] - the_map.map[i][j+1]     # on y
            n = math.sqrt(v1**2 + v2**2 + 1)
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
    zoomFactor = 1
    orient = 40.
    translateSpeed = [0, 0, 0]
    translation = [0, 0, 0]

    # Boucle Principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    autoRotate = False
                elif event.unicode in 'zqsdae':
                    autoRotate = False
                    
                if event.key == pygame.K_LEFT:
                    LRSpeed -= 1
                elif event.key == pygame.K_RIGHT:
                    LRSpeed += 1
                elif event.key == pygame.K_UP:
                    UDSpeed -= 1
                elif event.key == pygame.K_DOWN:
                    UDSpeed += 1
                elif event.key == pygame.K_RETURN:
                    if UDSpeed == 0 and LRSpeed == 0:
                        autoRotate = not autoRotate
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == 270:
                    zoomFactor *= 1.1
                elif event.key == 269:
                    zoomFactor /= 1.1
                elif event.key == ord('z'):
                    translateSpeed[1] += 1
                elif event.key == ord('q'):
                    translateSpeed[0] -= 1
                elif event.key == ord('s'):
                    translateSpeed[1] -= 1
                elif event.key == ord('d'):
                    translateSpeed[0] += 1
                elif event.key == ord('a'):
                    translateSpeed[2] -= 1
                elif event.key == ord('e'):
                    translateSpeed[2] += 1
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    autoRotate = False
                if event.key == pygame.K_LEFT:
                    LRSpeed += 1
                elif event.key == pygame.K_RIGHT:
                    LRSpeed -= 1
                elif event.key == pygame.K_UP:
                    UDSpeed += 1
                elif event.key == pygame.K_DOWN:
                    UDSpeed -= 1
                elif event.key == ord('z'):
                    translateSpeed[1] -= 1
                elif event.key == ord('q'):
                    translateSpeed[0] += 1
                elif event.key == ord('s'):
                    translateSpeed[1] += 1
                elif event.key == ord('d'):
                    translateSpeed[0] -= 1
                elif event.key == ord('a'):
                    translateSpeed[2] += 1
                elif event.key == ord('e'):
                    translateSpeed[2] -= 1
            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 0)
        
        glPushMatrix()
        glTranslatef(0.0,0.0, -5)
        glTranslatef(translation[0], translation[1], translation[2])
        glRotated(orient, 1, 0, 0)
        glRotated(angle, 0, 1, 0)
        
        glScalef(zoomFactor, zoomFactor, zoomFactor)
        glLightiv(GL_LIGHT0,GL_POSITION,[0, 50, 0, 0])
        glTranslatef(-1, 0, -1)
        glScalef(2/the_map.side, 1, 2/the_map.side)
        glColor3f(0.1, 0.1, 0.1)
        
        glCallList(index)
        glPopMatrix()
        
        pygame.display.flip()
        if autoRotate:
            #angle += .2
            pass
        else:
            angle += 0.5*LRSpeed
            orient += 0.2*UDSpeed
            translation[0] += translateSpeed[0]*0.02
            translation[1] += translateSpeed[1]*0.02
            translation[2] += translateSpeed[2]*0.02
        pygame.time.wait(10)
    glDeleteLists(index, 1)
    pygame.quit()

