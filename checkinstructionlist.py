import sys

epsilon = 0.00001
positiontable = [0, 10, 44, 73, 102, 157, 184, 212, 240, 267, 294, 324, 377, 406, 434, 463, 490, 546, 574, 599, 624, 651, 673, 698, 749, 771, 798, 820, 846, 894, 919, 945, 969, 993, 1018, 1044, 1092, 1118, 1142, 1167, 1193, 1240, 1266, 1291, 1315, 1339, 1364, 1385, 1385]

def checkinstructionlist(instructionlist):
    class Arm:
        def __init__(self, position):
            self.position = position
            self.ismoving = False
            self.speed = 0.0
            self.instructionqueue = []

    instructionlist = sorted(instructionlist, key=lambda x: x[0])
    totaltime = instructionlist[-1][0]
    arms = [Arm(positiontable[0]), Arm(positiontable[2]), Arm(positiontable[-4]), Arm(positiontable[-2])]
    for instruction in instructionlist:
        arms[instruction[1]].instructionqueue.append(instruction)
    for time in range(totaltime):
        for arm in arms:
            if len(arm.instructionqueue) > 0:
                if arm.ismoving:
                    arm.position += arm.speed
                    if abs(arm.instructionqueue[0][2] - arm.position) < epsilon:
                        arm.instructionqueue.pop(0)
                        arm.ismoving = False
                else:
                    remainingtime = arm.instructionqueue[0][0] - time
                    if remainingtime - 490 < epsilon:
                        arm.ismoving = True
                        arm.speed = (arm.instructionqueue[0][2] - arm.position) / remainingtime
                        arm.position += arm.speed
                        if abs(arm.instructionqueue[0][2] - arm.position) < epsilon:
                            arm.instructionqueue.pop(0)
                            arm.ismoving = False
        if arms[1].position - arms[0].position < 15.0:
            print("Arm 0 collides with arm 1 at", time, "ms", file=sys.stderr)
            return
        elif arms[2].position - arms[1].position < 55.5:
            print("Arm 1 collides with arm 2 at", time, "ms", file=sys.stderr)
            return
        elif arms[3].position - arms[2].position < 15.0:
            print("Arm 2 collides with arm 3 at", time, "ms", file=sys.stderr)
            return
    print("Simulation successful")

if __name__ == "__main__":
    testlist = [(500, 1, positiontable[16]), (750, 2, positiontable[15])]
    checkinstructionlist(testlist)
