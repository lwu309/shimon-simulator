import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *

def writetext(x, y, text):
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glTranslatef(x, y, 0.0)
    glScalef(0.001, 0.001, 0.001)
    glColor3f(1.0, 1.0, 1.0)
    for c in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
    glPopMatrix()

def draw(x, y, time, fps):
    writetext(x, y, f'Time: {time}')
    writetext(x + 0.05, y - 0.14, f'FPS: {fps}')
