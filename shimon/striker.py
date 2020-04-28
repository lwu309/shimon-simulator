class Striker:
    def __init__(self, number):
        self.number = number
        self.armnumber = (number + 1) // 2
        self.lasthittime = -1
        self.isdead = False
        self.deadcounter = 0
        self.instructionqueue = []
        self.isblack = number % 2 == 1
