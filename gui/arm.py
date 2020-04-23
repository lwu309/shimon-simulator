import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *

import shimon.arm

def positiontox(position):
    return 1.89 * position / 1385 - 0.945

def draw(arms):
    for arm in arms:
        x = positiontox(arm.position)
        left = x - 0.01
        right = x + 0.01
        top = 0.2
        bottom = -0.7

        glColor3f(0.7, 0.7, 0.7)
        glBegin(GL_QUADS)
        glVertex3f(right, top, 0.0)
        glVertex3f(left, top, 0.0)
        glVertex3f(left, bottom, 0.0)
        glVertex3f(right, bottom, 0.0)
        glEnd()
