import argparse
import copy
import sys

import gui
import shimon.arm
import shimon.striker
import checkmidi
import log

def initialize(instructionlist, startpositions=[shimon.arm.positiontable[0], shimon.arm.positiontable[2], shimon.arm.positiontable[-4], shimon.arm.positiontable[-2]], strikercommands=None, midifilename=None, infofilename='guiinfo.log', warningfilename='guiwarning.log'):
    # Open log output
    log.open(infofilename, warningfilename)

    # Arm initialization
    instructionlist = sorted(instructionlist, key=lambda x: x[0])
    gui.totaltime = instructionlist[-1][0] + 2000
    gui.arms = [shimon.arm.Arm(1, startpositions[0]), shimon.arm.Arm(2, startpositions[1]), shimon.arm.Arm(3, startpositions[2]), shimon.arm.Arm(4, startpositions[3])]
    for instruction in instructionlist:
        gui.arms[instruction[1] - 1].instructionqueue.append(instruction)

    # Striker initialization
    for i in range(8):
        gui.strikers.append(shimon.striker.Striker(i + 1))
    if strikercommands is not None and len(strikercommands) > 0:
        strikercommands = sorted(strikercommands, key=lambda x: x[0])
        gui.strikercommands = strikercommands
        strikermaxtime = int(strikercommands[-1][0]) + 2000
        if gui.totaltime < strikermaxtime:
            gui.totaltime = strikermaxtime
        for strikercommand in strikercommands:
            for i in range(8):
                if strikercommand[i + 1] == 1:
                    gui.strikers[i].instructionqueue.append(strikercommand[0])
        if midifilename is not None:
            gui.numberofnotes, gui.notelist = checkmidi.readnotes(midifilename)
            gui.offset = checkmidi.findstaticoffset(strikercommands[0][0] + 85, gui.notelist)
            print('Static offset:', gui.offset, file=sys.stderr)
            gui.midifilename = midifilename

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--armfile')
    parser.add_argument('--strikerfile')
    parser.add_argument('--midifile')
    parser.add_argument('--arm1position', type=int)
    parser.add_argument('--arm2position', type=int)
    parser.add_argument('--arm3position', type=int)
    parser.add_argument('--arm4position', type=int)
    args = parser.parse_args()
    if args.armfile is None:
        print('Please specify at least an arm message file', file=sys.stderr)
    else:
        armlist = []
        armfile = open(args.armfile, 'r')
        for line in armfile:
            tokens = line.split()
            armlist.append([int(tokens[7]), int(tokens[1]), int(tokens[2]), float(tokens[3]), float(tokens[4])])
        armfile.close()
        if args.arm1position is not None and args.arm2position is not None and args.arm3position is not None and args.arm4position is not None:
            startpositions = [args.arm1position, args.arm2position, args.arm3position, args.arm4position]
        else:
            startpositions = [shimon.arm.positiontable[0], shimon.arm.positiontable[2], shimon.arm.positiontable[-4], shimon.arm.positiontable[-2]]
        if args.strikerfile is None:
            initialize(armlist, startpositions=startpositions)
        else:
            strikerlist = []
            strikerfile = open(args.strikerfile, 'r')
            for line in strikerfile:
                tokens = line.split()
                if tokens[0] != 'p':
                    strikerlist.append([int(tokens[12]), int(tokens[8]), int(tokens[7]), int(tokens[6]), int(tokens[5]), int(tokens[4]), int(tokens[3]), int(tokens[2]), int(tokens[1])])
            strikerfile.close()
            initialize(armlist, startpositions=startpositions, strikercommands=strikerlist, midifilename=args.midifile)
    gui.main()
