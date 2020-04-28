import os
import sys

import shimon.arm
import checkinstructionlist

def runtest():
    print('Test case: Four arms moving together', file=sys.stderr)
    infofilename = 'test.log'
    armlist = []
    armlist.append([0, 1, 1018, 0.421, 959])
    armlist.append([0, 2, 1118, 0.421, 959])
    armlist.append([0, 3, 1240, 0.421, 959])
    armlist.append([0, 4, 1315, 0.421, 959])
    
    checkinstructionlist.checkinstructionlist(armlist, startpositions=[shimon.arm.positiontable[0], shimon.arm.positiontable[2], shimon.arm.positiontable[7], shimon.arm.positiontable[9]], infofilename=infofilename, warningfilename=None)
    log = open(infofilename, 'r')
    logstring = log.read()
    log.close()
    if logstring == 'Arm 1 shifts to STARTING state at time 0\nArm 2 shifts to STARTING state at time 0\nArm 3 shifts to STARTING state at time 0\nArm 4 shifts to STARTING state at time 0\nArm 1 shifts to ACCELERATING state at time 34\nArm 2 shifts to ACCELERATING state at time 34\nArm 3 shifts to ACCELERATING state at time 34\nArm 4 shifts to ACCELERATING state at time 34\nArm 1 shifts to MOVING state at time 267\nArm 2 shifts to MOVING state at time 267\nArm 3 shifts to MOVING state at time 267\nArm 4 shifts to MOVING state at time 267\nArm 1 shifts to DECELERATING state at time 1207\nArm 1 shifts to WAITING state at time 1217\nArm 3 shifts to DECELERATING state at time 1218\nArm 3 shifts to WAITING state at time 1228\nArm 4 shifts to DECELERATING state at time 1239\nArm 4 shifts to WAITING state at time 1249\nArm 2 shifts to DECELERATING state at time 1266\nArm 2 shifts to WAITING state at time 1276\nSimulation successful\n':
        print('Test passed', file=sys.stderr)
    else:
        print('Test failed', file=sys.stderr)
    if os.path.exists(infofilename):
        os.remove(infofilename)

if __name__ == '__main__':
    runtest()
