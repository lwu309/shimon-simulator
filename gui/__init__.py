import sys
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import gui.arm
import gui.keyboard
import gui.stats

import sound

import cycle
import shimon.arm

window_width = 1.0
window_height = 1.0

frame = 0
starttime = 0
basetime = 0
time = 0
fps = 0

paused = False

arms = []
strikers = []
strikercommands = []
totaltime = 0
numberofnotes = 0
notelist = []
offset = 0
midifilename = None
info = None
warning = None
hitnotes = []

startcycle = 0
stop = False

def idleFunc():
    global frame
    global starttime
    global basetime
    global time
    global fps

    global arms
    global strikers
    global strikercommands
    global totaltime
    global numberofnotes
    global notelist
    global offset
    global midifilename
    global info
    global warning
    global hitnotes

    global startcycle
    global stop

    if not stop:
        # Draw current frame
        glutPostRedisplay()

        elapsed_time = glutGet(GLUT_ELAPSED_TIME)

        startcycle = time
        if frame == 0:
            starttime = elapsed_time
            basetime = elapsed_time
            time = starttime
            fps = 0
        else:
            if not paused:
                time = elapsed_time - starttime
            else:
                starttime = elapsed_time - time
            if (elapsed_time - basetime > 1000):
                fps = int(round(frame * 1000 / (elapsed_time - basetime)))
                basetime = elapsed_time
                frame = 0
            if time >= totaltime:
                time = totaltime
                stop = True
            if not paused:
                cyclesuccess, hitnotes = cycle.runcycle(arms, strikers, strikercommands, startcycle, time, numberofnotes, notelist, offset, midifilename, info, warning)
                # Play hit notes
                for note in hitnotes:
                    sound.play(note)
                if not cyclesuccess:
                    gui.arm.crashedarms = hitnotes
                    stop = True
                    glutPostRedisplay()
                else:
                    if time == totaltime:
                        info.write('Simulation successful\n')
                        info.close()
    frame += 1

def displayFunc():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    gui.stats.draw(-window_width + 0.02, window_height - 0.08, time, fps)
    arm = shimon.arm.Arm(1, 44)
    gui.arm.draw(arms, strikers, cycle.strikerhits)
    gui.keyboard.hitnotes = hitnotes
    gui.keyboard.draw()
    glutSwapBuffers()

def keyboardFunc(key, x, y):
    global paused
    if key == b' ':
        paused = not paused

def reshapeFunc(width, height):
    global window_width
    global window_height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if width > height:
        window_height = 1.0
        window_width = width / height
    else:
        window_width = 1.0
        window_height = height / width
    gluOrtho2D(-window_width, window_width, -window_height, window_height)
    glMatrixMode(GL_MODELVIEW)
    glViewport(0, 0, width, height)

def main():
    # Initialize GLUT window
    glutInit()
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_MULTISAMPLE)
    glutInitWindowPosition(50, 50)
    glutInitWindowSize(800, 600)
    glutCreateWindow('Shimon simulator')
    glutIdleFunc(idleFunc)
    glutDisplayFunc(displayFunc)
    glutKeyboardFunc(keyboardFunc)
    glutReshapeFunc(reshapeFunc)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)
    glLineWidth(2.0)
    glClearColor(0.25, 0.4, 0.25, 1.0)
    glPolygonMode(GL_FRONT, GL_FILL)

    # Start sound
    sound.start()

    glutMainLoop()
