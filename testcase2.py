import os
import sys

import checkinstructionlist

def runtest():
    print('Test case: Arm 1 crashes Arm 2 (same direction)', file=sys.stderr)
    infofilename = 'test.log'
    armlist = []
    armlist.append([0, 1, 267, 0.421, 959])
    armlist.append([0, 2, 377, 0.3, 750])
    
    checkinstructionlist.checkinstructionlist(armlist, infofilename=infofilename, warningfilename=None)
    log = open(infofilename, 'r')
    logstring = log.read()
    log.close()
    if logstring == 'Arm 1 shifts to STARTING state at time 0\nArm 2 shifts to STARTING state at time 0\nArm 1 shifts to ACCELERATING state at time 34\nArm 2 shifts to ACCELERATING state at time 34\nError: Arm 1 collides with arm 2 at 256 ms\n':
        print('Test passed', file=sys.stderr)
    else:
        print('Test failed', file=sys.stderr)
    if os.path.exists(infofilename):
        os.remove(infofilename)

if __name__ == '__main__':
    runtest()
