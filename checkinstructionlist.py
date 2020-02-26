import enum
import sys

positiontable = [0, 10, 44, 73, 102, 157, 184, 212, 240, 267, 294, 324, 377, 406, 434, 463, 490, 546, 574, 599, 624, 651, 673, 698, 749, 771, 798, 820, 846, 894, 919, 945, 969, 993, 1018, 1044, 1092, 1118, 1142, 1167, 1193, 1240, 1266, 1291, 1315, 1339, 1364, 1385, 1385]

def checkinstructionlist(instructionlist, startpositions=[positiontable[0], positiontable[2], positiontable[-4], positiontable[-2]]):
    class Arm:
        def __init__(self, position):
            self.position = position
            self.state = ArmState.WAITING
            self.speed = 0.0
            self.direction = 1
            self.instructionqueue = []
            self.waittime = 35

    class ArmState(enum.Enum):
        WAITING = 0
        STARTING = 1
        ACCELERATING = 2
        MOVING = 3
        DECELERATING = 4

    instructionlist = sorted(instructionlist, key=lambda x: x[0])
    totaltime = instructionlist[-1][0] + 1000
    arms = [Arm(startpositions[0]), Arm(startpositions[1]), Arm(startpositions[2]), Arm(startpositions[3])]
    for instruction in instructionlist:
        instruction[3] *= 0.0098 # m/s^2/9.8 -> mm/ms^2
        instruction[4] /= 1000.0 # mm/s -> mm/ms
        arms[instruction[1] - 1].instructionqueue.append(instruction)
    for time in range(-1, totaltime):
        for arm in arms:
            if len(arm.instructionqueue) > 0:
                if arm.state == ArmState.WAITING:
                    if time == arm.instructionqueue[0][0] - 1:
                        arm.state = ArmState.STARTING
                    elif time > arm.instructionqueue[0][0]:
                        print('Warning: Arm', arm.instructionqueue[0][1], 'tries to execute instruction received at time', arm.instructionqueue[0][0], 'ms late at time', time, 'ms', file=sys.stderr)
                        if time >= arm.instructionqueue[0][0] + 35:
                            arm.waittime = 1
                        else:
                            arm.waittime = 35 - (time - arm.instructionqueue[0][0])
                        arm.state = ArmState.STARTING
                elif arm.state == ArmState.STARTING:
                    if abs(arm.instructionqueue[0][2] - arm.position) < sys.float_info.epsilon:
                        arm.position = arm.instructionqueue[0][2]
                        arm.instructionqueue.pop(0)
                        arm.state = ArmState.WAITING
                        arm.waittime = 35
                    else:
                        arm.waittime -= 1
                        if arm.waittime == 0:
                            arm.state = ArmState.ACCELERATING
                            if arm.instructionqueue[0][2] > arm.position:
                                arm.direction = 1
                            elif arm.instructionqueue[0][2] < arm.position:
                                arm.direction = -1
                elif arm.state == ArmState.ACCELERATING:
                    arm.position += arm.speed + 0.5 * arm.direction * arm.instructionqueue[0][3]
                    arm.speed += arm.direction * arm.instructionqueue[0][3]
                    if arm.direction == 1 and arm.position - arm.instructionqueue[0][2] > sys.float_info.epsilon or arm.direction == -1 and arm.instructionqueue[0][2] - arm.position > sys.float_info.epsilon:
                        print('Warning: Arm', arm.instructionqueue[0][1], 'moves beyond target position on acceleration\n    Time:', time, '\n    Target position:', arm.instructionqueue[0][2], '\n    Position:', arm.position, file=sys.stderr)
                        arm.instructionqueue.pop(0)
                        arm.state = ArmState.WAITING
                        arm.waittime = 35
                    elif abs(arm.speed) > 2.5:
                        arm.speed = 2.5 if arm.direction == 1 else -2.5
                    elif abs(arm.speed) >= abs(arm.instructionqueue[0][4]):
                        arm.speed = arm.direction * arm.instructionqueue[0][4]
                        arm.state = ArmState.MOVING
                elif arm.state == ArmState.MOVING:
                    arm.position += arm.speed
                    if arm.direction == 1:
                        if arm.position - arm.instructionqueue[0][2] > sys.float_info.epsilon:
                            print('Warning: Arm', arm.instructionqueue[0][1], 'moves beyond target position on constant speed motion\n    Time:', time, '\n    Target position:', arm.instructionqueue[0][2], '\n    Position:', arm.position, file=sys.stderr)
                        if arm.instructionqueue[0][2] - arm.position <= 0.5 * arm.instructionqueue[0][3] * ((arm.instructionqueue[0][4] / arm.instructionqueue[0][3]) ** 2):
                            arm.state = ArmState.DECELERATING
                    elif arm.direction == -1:
                        if arm.instructionqueue[0][2] - arm.position > sys.float_info.epsilon:
                            print('Warning: Arm', arm.instructionqueue[0][1], 'moves beyond target position on constant speed motion\n.   Time:', time, '\n    Target position:', arm.instructionqueue[0][2], '\n    Position:', arm.position, file=sys.stderr)
                        if arm.position - arm.instructionqueue[0][2] <= 0.5 * arm.instructionqueue[0][3] * ((arm.instructionqueue[0][4] / arm.instructionqueue[0][3]) ** 2):
                            arm.state = ArmState.DECELERATING
                elif arm.state == ArmState.DECELERATING:
                    arm.position += arm.speed + 0.5 * -arm.direction * arm.instructionqueue[0][3]
                    arm.speed += -arm.direction * arm.instructionqueue[0][3]
                    if arm.direction == 1 and (arm.position > arm.instructionqueue[0][2] or abs(arm.position - arm.instructionqueue[0][2]) < sys.float_info.epsilon) or arm.direction == -1 and (arm.position < arm.instructionqueue[0][2] or abs(arm.position - arm.instructionqueue[0][2]) < sys.float_info.epsilon):
                        arm.instructionqueue.pop(0)
                        arm.state = ArmState.WAITING
                        arm.speed = 0.0
                        arm.waittime = 35
        if arms[1].position - arms[0].position < 15.0:
            print("Arm 1 collides with arm 2 at", time, "ms", file=sys.stderr)
            return
        elif arms[2].position - arms[1].position < 55.5:
            print("Arm 2 collides with arm 3 at", time, "ms", file=sys.stderr)
            return
        elif arms[3].position - arms[2].position < 15.0:
            print("Arm 3 collides with arm 4 at", time, "ms", file=sys.stderr)
            return
    print("Simulation successful")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python[3] checkinstructionlist.py filename [[arm 1 position] [arm 2 position] [arm 3 position] [arm 4 position]]", file=sys.stderr)
    else:
        testlist = []
        testfile = open(sys.argv[1], 'r')
        for line in testfile:
            tokens = line.split()
            testlist.append([int(tokens[7]), int(tokens[1]), int(tokens[2]), float(tokens[3]), float(tokens[4])])
        if len(sys.argv) == 2:
            checkinstructionlist(testlist)
        else:
            checkinstructionlist(testlist, startpositions=[int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])])
