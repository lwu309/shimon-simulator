import copy
import sys
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import gui.arm
import gui.keyboard
import gui.stats

import sound

import shimon.arm
import cycle
import log

# GUI states
window_width = 1.0
window_height = 1.0

frame = 0
starttime = 0
basetime = 0
time = 0
fps = 0

paused = False

# Simulation states
arms = []
strikers = []
strikercommands = []
totaltime = 0
numberofnotes = 0
notelist = []
offset = 0
midifilename = None

startcycle = 0
stop = False

initialarms = []
initialstrikers = []

def idleFunc():
    global frame
    global starttime
    global basetime
    global time
    global fps

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
                cyclesuccess, crashedarms = cycle.run(arms, strikers, strikercommands, startcycle, time, numberofnotes, notelist, offset, midifilename)
                # Play hit notes
                for notehit in cycle.notehits:
                    if not notehit[2]:
                        # Hitvel is yet to be implemented, assign a static 127
                        sound.play(notehit[0], 127)
                        notehit[2] = True
                if not cyclesuccess:
                    gui.arm.crashedarms = crashedarms
                    stop = True
                    glutPostRedisplay()
                    log.close()
                else:
                    if time == totaltime:
                        log.info('Simulation successful')
                        log.close()
    frame += 1

def displayFunc():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    gui.stats.draw(-window_width + 0.02, window_height - 0.08, time, fps)
    arm = shimon.arm.Arm(1, 44)
    gui.arm.draw(arms, strikers, cycle.strikerhits)
    gui.keyboard.draw(cycle.notehits)
    glutSwapBuffers()

def keyboardFunc(key, x, y):
    global starttime
    global time
    global paused
    global arms
    global strikers
    global stop

    # Space to pause
    if key == b' ':
        paused = not paused
    # R to restart simulation
    elif key in [b'r', b'R']:
        log.info('Restart simulation')
        for i in range(len(arms)):
            arms[i].number = initialarms[i].number
            arms[i].position = initialarms[i].position
            arms[i].state = initialarms[i].state
            arms[i].speed = initialarms[i].speed
            arms[i].direction = initialarms[i].direction
            arms[i].instructionqueue = copy.deepcopy(initialarms[i].instructionqueue)
            arms[i].waittime = initialarms[i].waittime
        for i in range(len(strikers)):
            strikers[i].number = initialstrikers[i].number
            strikers[i].armnumber = initialstrikers[i].armnumber
            strikers[i].lasthittime = initialstrikers[i].lasthittime
            strikers[i].isdead = initialstrikers[i].isdead
            strikers[i].deadcounter = initialstrikers[i].deadcounter
            strikers[i].instructionqueue = copy.deepcopy(initialstrikers[i].instructionqueue)
            strikers[i].isblack = initialstrikers[i].isblack
        elapsed_time = glutGet(GLUT_ELAPSED_TIME)
        starttime = elapsed_time
        time = 0
        cycle.notehits.clear()
        cycle.strikerhits.clear()
        stop = False

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
    global initialarms
    global initialstrikers

    # Make deep copies for arms and strikers
    initialarms = copy.deepcopy(arms)
    initialstrikers = copy.deepcopy(strikers)

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
