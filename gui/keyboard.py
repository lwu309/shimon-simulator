import OpenGL
from OpenGL.GL import *

from gui.arm import positiontox

import shimon.arm

whitesubindex = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}
blackoffset = {1: 0.05, 3: 0.12, 6: 0.26, 8: 0.33, 10: 0.40}

def isblack(note):
    return note % 12 in [1, 3, 6, 8, 10]

def drawkey(note, ishit):
    center = positiontox(shimon.arm.positiontable[note - 48])
    glBegin(GL_QUADS)
    if isblack(note):
        left = center - 0.02
        right = center + 0.02
        top = 0.7
        bottom = 0.1
        if ishit:
            glColor3f(1.0, 0.7, 0.0)
        else:
            glColor3f(0.0, 0.0, 0.0)
        glVertex3f(left, top, 0.0)
        glVertex3f(left, bottom, 0.0)
        glVertex3f(right, bottom, 0.0)
        glVertex3f(right, top, 0.0)
    else:
        subindex = whitesubindex[note % 12]
        left = 0.0
        right = 0.0
        if subindex in [0, 3]:
            diffinc = positiontox(shimon.arm.positiontable[note - 46]) - center
            diffdec = center - positiontox(shimon.arm.positiontable[note - 49])
            left = -0.98 if note == 48 else (center - diffdec / 2)
            right = center + diffinc / 2
        elif subindex in [1, 4, 5]:
            diffinc = positiontox(shimon.arm.positiontable[note - 46]) - center
            diffdec = center - positiontox(shimon.arm.positiontable[note - 50])
            left = center - diffdec / 2
            right = center + diffinc / 2
        else:
            diffinc = positiontox(shimon.arm.positiontable[note - 47]) - center
            diffdec = center - positiontox(shimon.arm.positiontable[note - 50])
            left = center - diffdec / 2
            right = 0.98 if note == 95 else (center + diffinc / 2)
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
        if ishit:
            glColor3f(1.0, 0.7, 0.0)
        else:
            glColor3f(1.0, 1.0, 1.0)
        glVertex3f(left, top, 0.0)
        glVertex3f(left, bottom, 0.0)
        glVertex3f(right, bottom, 0.0)
        glVertex3f(right, top, 0.0)
    glEnd()

def draw(notehits):
    # Draw black keys first
    for i in range(48, 96):
        if (isblack(i)):
            drawkey(i, i in [notehit[0] for notehit in notehits])
    # Draw white keys
    for i in range(48, 96):
        if not isblack(i):
            drawkey(i, i in [notehit[0] for notehit in notehits])
