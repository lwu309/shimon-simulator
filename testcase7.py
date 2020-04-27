import os
import sys

import checkinstructionlist

def runtest():
    print('Test case: Striker hit during movement', file=sys.stderr)
    infofilename = 'test.log'
    armlist = []
    armlist.append([0, 3, 798, 0.421, 959])
    strikerlist = []
    strikerlist.append([555, 0, 0, 0, 0, 1, 0, 0, 0])
    
    checkinstructionlist.checkinstructionlist(armlist, strikercommands=strikerlist, infofilename=infofilename)
    log = open(infofilename, 'r')
    logstring = log.read()
    log.close()
    if logstring == 'Arm 3 shifts to STARTING state at time 0\nArm 3 shifts to ACCELERATING state at time 34\nArm 3 shifts to MOVING state at time 267\nStriker 5 hits the keyboard at time 640 on note 77\nArm 3 shifts to DECELERATING state at time 736\nArm 3 shifts to WAITING state at time 746\nSimulation successful\n':
        print('Test passed', file=sys.stderr)
    else:
        print('Test failed', file=sys.stderr)
    if os.path.exists(infofilename):
        os.remove(infofilename)

if __name__ == '__main__':
    runtest()
