import os
import sys

import checkinstructionlist

def runtest():
    print('Test case: Arm 2 moves right-hand', file=sys.stderr)
    logfilename = 'test.log'
    armlist = []
    armlist.append([0, 2, 698, 0.421, 959])
    
    checkinstructionlist.checkinstructionlist(armlist, logfilename=logfilename)
    log = open(logfilename, 'r')
    logstring = log.read()
    log.close()
    if logstring == 'Arm 2 shifts to STARTING state at time 0\nArm 2 shifts to ACCELERATING state at time 34\nArm 2 shifts to MOVING state at time 267\nArm 2 shifts to DECELERATING state at time 828\nArm 2 shifts to WAITING state at time 838\nSimulation successful\n':
        print('Test passed', file=sys.stderr)
    else:
        print('Test failed', file=sys.stderr)
    if os.path.exists(logfilename):
        os.remove(logfilename)

if __name__ == '__main__':
    runtest()
