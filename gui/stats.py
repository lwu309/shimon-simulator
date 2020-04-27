import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *

def writetext(x, y, text):
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glTranslatef(x, y, 0.0)
    glScalef(0.0005, 0.0005, 0.0005)
    glColor3f(1.0, 1.0, 1.0)
    for c in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
    glPopMatrix()

def draw(x, y, time, fps):
    writetext(x, y, f'Time: {time // 1000}.{time % 1000:03d}')
    writetext(x + 0.025, y - 0.08, f'FPS: {fps}')
