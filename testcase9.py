import os
import sys

import checkinstructionlist

def runtest():
    print('Test case: Striker hit much after movement', file=sys.stderr)
    logfilename = 'test.log'
    armlist = []
    armlist.append([0, 3, 798, 0.421, 959])
    strikerlist = []
    strikerlist.append([960, 0, 0, 0, 0, 1, 0, 0, 0])
    
    checkinstructionlist.checkinstructionlist(armlist, strikercommands=strikerlist, logfilename=logfilename)
    log = open(logfilename, 'r')
    logstring = log.read()
    log.close()
    if logstring == 'Arm 3 shifts to STARTING state at time 0\nArm 3 shifts to ACCELERATING state at time 34\nArm 3 shifts to MOVING state at time 267\nArm 3 shifts to DECELERATING state at time 736\nArm 3 shifts to WAITING state at time 746\nStriker 5 hits the keyboard at time 1045 on note 74\nSimulation successful\n':
        print('Test passed', file=sys.stderr)
    else:
        print('Test failed', file=sys.stderr)
    if os.path.exists(logfilename):
        os.remove(logfilename)

if __name__ == '__main__':
    runtest()
