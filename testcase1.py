import os
import sys

import checkinstructionlist

def runtest():
    print('Test case: Arm 1 moving right-hand with Arm 2', file=sys.stderr)
    infofilename = 'test.log'
    armlist = []
    armlist.append([0, 1, 267, 0.421, 959])
    armlist.append([0, 2, 377, 0.421, 959])
    
    checkinstructionlist.checkinstructionlist(armlist, infofilename=infofilename)
    log = open(infofilename, 'r')
    logstring = log.read()
    log.close()
    if logstring == 'Arm 1 shifts to STARTING state at time 0\nArm 2 shifts to STARTING state at time 0\nArm 1 shifts to ACCELERATING state at time 34\nArm 2 shifts to ACCELERATING state at time 34\nArm 1 shifts to MOVING state at time 267\nArm 2 shifts to MOVING state at time 267\nArm 1 shifts to DECELERATING state at time 424\nArm 1 shifts to WAITING state at time 434\nArm 2 shifts to DECELERATING state at time 493\nArm 2 shifts to WAITING state at time 503\nSimulation successful\n':
        print('Test passed', file=sys.stderr)
    else:
        print('Test failed', file=sys.stderr)
    if os.path.exists(infofilename):
        os.remove(infofilename)

if __name__ == '__main__':
    runtest()
