import enum

positiontable = [0, 10, 44, 73, 102, 157, 184, 212, 240, 267, 294, 324, 377, 406, 434, 463, 490, 546, 574, 599, 624, 651, 673, 698, 749, 771, 798, 820, 846, 894, 919, 945, 969, 993, 1018, 1044, 1092, 1118, 1142, 1167, 1193, 1240, 1266, 1291, 1315, 1339, 1364, 1385, 1385]

class Arm:
    def __init__(self, number, position):
        self.number = number
        self.position = position
        self.state = ArmState.WAITING
        self.speed = 0.0
        self.direction = 1
        self.instructionqueue = []
        self.waittime = 35
    def currentinstructiontime(self):
        return self.instructionqueue[0][0]
    def currentinstructiontargetposition(self):
        return self.instructionqueue[0][2]
    def currentinstructionacceleration(self):
        return self.instructionqueue[0][3] * 0.0098 # m/s^2/9.8 -> mm/ms^2
    def currentinstructiontargetspeed(self):
        return self.instructionqueue[0][4] / 1000.0 # mm/s -> mm/ms
    def nextinstructiontime(self):
        return self.instructionqueue[1][0] if len(self.instructionqueue) > 1 else None
    def deceleration(self):
        return 9.8 * 0.0098
    def reportlog(self, log):
        log.write(f'Arm {self.number}:\n    Position: {self.position}\n    Speed: {self.speed}\n    State: {self.state}\n    Message:\n        Time: {self.instructionqueue[0][0]}\n        Target position: {self.instructionqueue[0][2]}\n        Acceleration: {self.instructionqueue[0][3]} m/s/9.8\n        Velocity: {self.instructionqueue[0][4]} mm/s\n')

class ArmState(enum.Enum):
    WAITING = 0
    STARTING = 1
    ACCELERATING = 2
    MOVING = 3
    DECELERATING = 4
