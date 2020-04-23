import OpenGL
from OpenGL.GL import *

whitesubindex = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}
blackoffset = {1: 0.05, 3: 0.12, 6: 0.26, 8: 0.33, 10: 0.40}

hitnotes = []

def isblack(note):
    return note % 12 in [1, 3, 6, 8, 10]

def drawkey(note):
    left = -0.9
    glBegin(GL_QUADS)
    if isblack(note):
        left = -0.98 + (note - 48) // 12 * 0.49 + blackoffset[note % 12]
        right = left + 0.04
        top = 0.7
        bottom = 0.1
        if note in hitnotes:
            glColor3f(1.0, 0.7, 0.0)
        else:
            glColor3f(0.0, 0.0, 0.0)
        glVertex3f(left, top, 0.0)
        glVertex3f(left, bottom, 0.0)
        glVertex3f(right, bottom, 0.0)
        glVertex3f(right, top, 0.0)
    else:
        index = (note - 48) // 12 * 7 + whitesubindex[note % 12]
        left = -0.98 + index * 0.07
        right = left + 0.07
        top = 0.7
        bottom = -0.3
        # Draw border
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(left - 0.0025, top + 0.0025, 0.0)
        glVertex3f(left - 0.0025, bottom - 0.0025, 0.0)
        glVertex3f(left + 0.0025, bottom - 0.0025, 0.0)
        glVertex3f(left + 0.0025, top + 0.0025, 0.0)
        glVertex3f(left - 0.0025, bottom + 0.0025, 0.0)
        glVertex3f(left - 0.0025, bottom - 0.0025, 0.0)
        glVertex3f(right + 0.0025, bottom - 0.0025, 0.0)
        glVertex3f(right + 0.0025, bottom + 0.0025, 0.0)
        glVertex3f(right - 0.0025, top + 0.0025, 0.0)
        glVertex3f(right - 0.0025, bottom - 0.0025, 0.0)
        glVertex3f(right + 0.0025, bottom - 0.0025, 0.0)
        glVertex3f(right + 0.0025, top + 0.0025, 0.0)
        glVertex3f(left - 0.0025, top + 0.0025, 0.0)
        glVertex3f(left - 0.0025, top - 0.0025, 0.0)
        glVertex3f(right + 0.0025, top - 0.0025, 0.0)
        glVertex3f(right + 0.0025, top + 0.0025, 0.0)
        # Draw the key
        if note in hitnotes:
            glColor3f(1.0, 0.7, 0.0)
        else:
            glColor3f(1.0, 1.0, 1.0)
        glVertex3f(left, top, 0.0)
        glVertex3f(left, bottom, 0.0)
        glVertex3f(right, bottom, 0.0)
        glVertex3f(right, top, 0.0)
    glEnd()
    

def draw():
    # Draw black keys first
    for i in range(48, 96):
        if (isblack(i)):
            drawkey(i)
    # Draw white keys
    for i in range(48, 96):
        if not isblack(i):
            drawkey(i)
