import os
import sys

import checkinstructionlist

def runtest():
    print('Test case: Arm 2 and Arm 3 moving towards each other', file=sys.stderr)
    infofilename = 'test.log'
    armlist = []
    armlist.append([0, 2, 624, 0.421, 959])
    armlist.append([0, 3, 698, 0.3, 750])
    
    checkinstructionlist.checkinstructionlist(armlist, infofilename=infofilename)
    log = open(infofilename, 'r')
    logstring = log.read()
    log.close()
    if logstring == 'Arm 2 shifts to STARTING state at time 0\nArm 3 shifts to STARTING state at time 0\nArm 2 shifts to ACCELERATING state at time 34\nArm 3 shifts to ACCELERATING state at time 34\nArm 2 shifts to MOVING state at time 267\nArm 3 shifts to MOVING state at time 290\nArm 2 shifts to DECELERATING state at time 751\nArm 2 shifts to WAITING state at time 761\nArm 3 shifts to DECELERATING state at time 1013\nArm 3 shifts to WAITING state at time 1021\nSimulation successful\n':
        print('Test passed', file=sys.stderr)
    else:
        print('Test failed', file=sys.stderr)
    if os.path.exists(infofilename):
        os.remove(infofilename)

if __name__ == '__main__':
    runtest()
