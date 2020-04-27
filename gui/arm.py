import math
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *

import shimon.arm
import shimon.striker

crashedarms = []

def positiontox(position):
    return 1.89 * position / 1385 - 0.945

def drawcircle(x, y, radius, sides=60):
    twopi = 2.0 * math.pi
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(0, sides + 1):
        glVertex2f(x + radius * math.cos(i * twopi / sides), y + radius * math.sin(i * twopi / sides))
    glEnd()

def draw(arms, strikers, strikerhits):
    for striker in strikers:
        x = positiontox(arms[striker.armnumber - 1].position)
        if striker.isdead:
            glColor3f(0.25, 0.25, 0.25)
        elif striker.number in [hit[0] for hit in strikerhits]:
            glColor3f(1.0, 1.0, 0.0)
        else:
            glColor3f(0.0, 0.0, 0.5)
        drawcircle(x, -0.1 if striker.number % 2 == 0 else 0.3, 0.03)
    for arm in arms:
        x = positiontox(arm.position)
        left = x - 0.01
        right = x + 0.01
        top = 0.3
        bottom = -0.7

        if arm.number in crashedarms:
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(0.7, 0.7, 0.7)
        glBegin(GL_QUADS)
        glVertex3f(right, top, 0.0)
        glVertex3f(left, top, 0.0)
        glVertex3f(left, bottom, 0.0)
        glVertex3f(right, bottom, 0.0)
        glEnd()
