import math
import sys

# The PyPI goto-statement package does not support Python 3.8 yet, using a third-party fork
from thirdparty.goto import with_goto

import shimon.arm
import shimon.striker
import checkmidi
import parameters

strikerhits = []

@with_goto
def runcycle(arms, strikers, strikercommands, startcycle, endcycle, numberofnotes, notelist, offset, midifilename, info, warning):
    def loginfo(logmessage):
        print(logmessage, file=sys.stderr)
        print(logmessage, file=info)

    def logwarning(logmessage):
        logmessage = 'Warning: ' + logmessage
        print(logmessage, file=sys.stderr)
        print(logmessage, file=info)
        print(logmessage, file=warning)

    def logerror(logmessage):
        logmessage = 'Error: ' + logmessage
        print(logmessage, file=sys.stderr)
        print(logmessage, file=info)
        print(logmessage, file=warning)

    hitnotes = []

    for time in range(startcycle, endcycle):
        # Arms
        for arm in arms:
            label .fsmstart
            # Run finite state machine for each arm when message queue is not empty
            if len(arm.instructionqueue) > 0:
                # Waiting state
                # Wait for next message for this specific arm to arrive.
                if arm.state == shimon.arm.ArmState.WAITING:
                    if time == arm.currentinstructiontime():
                        # Drop the message if the target position is invalid
                        if arm.currentinstructiontargetposition() < shimon.arm.positiontable[0] or arm.currentinstructiontargetposition() > shimon.arm.positiontable[-1]:
                            logwarning(f'Arm {arm.number} receives message with invalid target position {arm.currentinstructiontargetposition()}, dropping instruction')
                            arm.instructionqueue.pop(0)
                            goto .fsmstart
                        # Keep only the latest message received at the same time
                        while len(arm.instructionqueue) > 1 and arm.nextinstructiontime() == arm.currentinstructiontime():
                            logwarning(f'Arm {arm.number} receives multiple instructions at time {time - offset}, dropping old instruction\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}')
                            arm.instructionqueue.pop(0)
                        # Shift to Starting state
                        arm.state = shimon.arm.ArmState.STARTING
                        print(f'Arm {arm.number} shifts to STARTING state at time {time - offset}', file=info)
                        goto .fsmstart # We need goto to shift state immediately at time 0

                # Starting state
                # Wait for 35 milliseconds before executing the command.
                elif arm.state == shimon.arm.ArmState.STARTING:
                    # Drop the current message on receiving next instruction in Starting state
                    if len(arm.instructionqueue) > 1 and time == arm.nextinstructiontime():
                        logwarning(f'Arm {arm.number} receives new instruction on starting state, dropping the current instruction\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}')
                        arm.instructionqueue.pop(0)
                        # Keep only the latest message received at the same time
                        while len(arm.instructionqueue) > 1 and arm.nextinstructiontime() == arm.currentinstructiontime():
                            logwarning(f'Arm {arm.number} receives multiple instructions at time {time - offset}, dropping old instruction\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}')
                            arm.instuctionqueue.pop(0)
                        # Reset wait time
                        arm.waittime = 35
                        goto .fsmstart
                    # If we are already at the target position, regard as complete and wait for next message
                    if abs(arm.currentinstructiontargetposition() - arm.position) < sys.float_info.epsilon:
                        arm.position = arm.currentinstructiontargetposition()
                        arm.instructionqueue.pop(0)
                        arm.state = shimon.arm.ArmState.WAITING
                        print(f'Arm {arm.number} shifts to WAITING state at time {time - offset}', file=info)
                        arm.waittime = 35
                        goto .fsmstart
                    # Otherwise, wait for 35 ms before starting to execute the command
                    else:
                        arm.waittime -= 1
                        if arm.waittime == 0:
                            # We don't have to shift state immediately so no goto here
                            arm.state = shimon.arm.ArmState.ACCELERATING
                            print(f'Arm {arm.number} shifts to ACCELERATING state at time {time - offset}', file=info)
                            # Set direction. 1 = right, -1 = left
                            if arm.currentinstructiontargetposition() > arm.position:
                                arm.direction = 1
                            elif arm.currentinstructiontargetposition() < arm.position:
                                arm.direction = -1

                # Accelerating state
                # Accelerate to the velocity specified
                elif arm.state == shimon.arm.ArmState.ACCELERATING:
                    # Drop the current message on receiving next instruction and shift to Starting state
                    if len(arm.instructionqueue) > 1 and time == arm.nextinstructiontime():
                        logwarning(f'Arm {arm.number} receives new instruction on accelerating state, dropping the current instruction\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}')
                        arm.instructionqueue.pop(0)
                        # Keep only the latest message received at the same time
                        while len(arm.instructionqueue) > 1 and arm.nextinstructiontime() == arm.currentinstructiontime():
                            logwarning(f'Warning: Arm {arm.number} receives multiple instructions at time {time - offset}, dropping old instruction\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}')
                            arm.instuctionqueue.pop(0)
                        arm.state = shimon.arm.ArmState.STARTING
                        print(f'Arm {arm.number} shifts to STARTING state at time {time - offset}', file=info)
                        # Reset wait time
                        arm.waittime = 35
                        goto .fsmstart
                    else:
                        acceleration = arm.direction * arm.currentinstructionacceleration()
                        newspeed = arm.speed + acceleration
                        maxspeed = min(arm.currentinstructiontargetspeed(), 2.5) # In magnitude
                        maxspeedtime = float('nan')
                        intermediateposition = float('nan')
                        newposition = arm.position + arm.speed + 0.5 * acceleration
                        # If we are reaching the maximum velocity in this cycle
                        if abs(newspeed) - maxspeed > sys.float_info.epsilon:
                            # Calculate the time elapsed to reach maximum velocity
                            maxspeedtime = (maxspeed - abs(arm.speed)) / arm.currentinstructionacceleration()
                            # Cap new speed
                            newspeed = arm.direction * maxspeed
                            # Calculate intermediate position and new position
                            intermediateposition = arm.position + arm.speed * maxspeedtime + 0.5 * acceleration * maxspeedtime ** 2
                            newposition = intermediateposition + newspeed * (1 - maxspeedtime)
                        # If we are moving past the target position in this cycle, jump to next message
                        if abs(newposition - arm.position) - abs(arm.currentinstructiontargetposition() - arm.position) > sys.float_info.epsilon:
                            logwarning(f'Arm {arm.number} moves beyond target position on acceleration\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}')
                            arm.position = arm.currentinstructiontargetposition()
                            arm.speed = 0
                            arm.instructionqueue.pop(0)
                            arm.state = shimon.arm.ArmState.WAITING
                            arm.waittime = 35
                            goto .fsmstart
                        else:
                            arm.position = newposition
                            arm.speed = newspeed
                        # Shift to Moving state after reaching maximum velocity
                        if abs(arm.speed - arm.direction * maxspeed) < sys.float_info.epsilon:
                            # We don't have to shift state immediately so no goto here
                            arm.state = shimon.arm.ArmState.MOVING
                            print(f'Arm {arm.number} shifts to MOVING state at time {time - offset}', file=info)

                # Moving state
                # Motion of constant speed
                elif arm.state == shimon.arm.ArmState.MOVING:
                    # Drop the current message on receiving next instruction and shift to Starting state
                    if len(arm.instructionqueue) > 1 and time == arm.nextinstructiontime():
                        logwarning(f'Arm {arm.number} receives new instruction on moving state, dropping the current instruction\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}')
                        arm.instructionqueue.pop(0)
                        # Keep only the latest message received at the same time
                        while len(arm.instructionqueue) > 1 and arm.nextinstructiontime() == arm.currentinstructiontime():
                            logwarning(f'Arm {arm.number} receives multiple instructions at time {time - offset}, dropping old instruction\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}')
                            arm.instuctionqueue.pop(0)
                        arm.state = shimon.arm.ArmState.STARTING
                        # Reset wait time
                        arm.waittime = 35
                        goto .fsmstart
                    else:
                        newspeed = arm.speed
                        intermediatetime = float('nan')
                        newposition = arm.position + arm.speed
                        decelerateposition = arm.currentinstructiontargetposition() - arm.direction * 0.5 * arm.deceleration() * (arm.currentinstructiontargetspeed() / arm.deceleration()) ** 2
                        """
                        # If we are moving past the target position in this cycle, jump to next message
                        if abs(newposition - arm.position) - abs(arm.currentinstructiontargetposition() - arm.position) > sys.float_info.epsilon:
                            print(f'Warning: Arm {arm.number} moves beyond target position on constant speed motion\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}', file=sys.stderr)
                            arm.position = arm.currentinstructiontargetposition()
                            arm.speed = 0
                            arm.instructionqueue.pop(0)
                            arm.state = shimon.arm.ArmState.WAITING
                            arm.waittime = 35
                            goto .fsmstart
                        """
                        # If we are reaching the position to start deceleration
                        if abs(newposition - arm.position) - abs(arm.currentinstructiontargetposition() - arm.position) > sys.float_info.epsilon or abs(newposition - arm.position) - abs(decelerateposition - arm.position) >= sys.float_info.epsilon:
                            # Calculate the time elapsed to reach decelerate position
                            intermediatetime = abs(decelerateposition - arm.position) / abs(arm.speed)
                            # If we can decelerate to zero velocity in this cycle, stop and wait for next message
                            if (1 - intermediatetime) - arm.currentinstructiontargetspeed() / arm.deceleration() >= sys.float_info.epsilon:
                                arm.position = arm.currentinstructiontargetposition()
                                arm.speed = 0.0
                                arm.instructionqueue.pop(0)
                                arm.state = shimon.arm.ArmState.WAITING
                                print(f'Arm {arm.number} shifts to WAITING state at time {time - offset}', file=info)
                                arm.waittime = 35
                                continue
                            # Calculate new position after deceleration
                            newposition = decelerateposition + arm.speed * (1 - intermediatetime) - arm.direction * 0.5 * arm.deceleration() * (1 - intermediatetime) ** 2
                            # Calculate new speed
                            newspeed = arm.speed - arm.direction * arm.deceleration() * (1 - intermediatetime)
                        arm.speed = newspeed
                        arm.position = newposition
                        # If we are reaching the position to start deceleration
                        if not math.isnan(intermediatetime) or abs(newposition - decelerateposition) < sys.float_info.epsilon:
                            # We don't have to shift state immediately so no goto here
                            arm.state = shimon.arm.ArmState.DECELERATING
                            print(f'Arm {arm.number} shifts to DECELERATING state at time {time - offset}', file=info)

                # Decelerating state
                # Deceleration to target position
                elif arm.state == shimon.arm.ArmState.DECELERATING:
                    if len(arm.instructionqueue) > 1 and time == arm.nextinstructiontime():
                        logwarning(f'Arm {arm.number} receives new instruction on decelerating state, dropping the current instruction\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}')
                        # Have to decelerate after all
                        arm.position = arm.currentinstructiontargetposition()
                        arm.instructionqueue.pop(0)
                        # Keep only the latest message received at the same time
                        while len(arm.instructionqueue) > 1 and arm.nextinstructiontime() == arm.currentinstructiontime():
                            logwarning(f'Arm {arm.number} receives multiple instructions at time {time - offset}, dropping old instruction\n    Time: {time - offset}\n    Target position: {arm.currentinstructiontargetposition()}\n    Position: {arm.position}')
                            arm.instuctionqueue.pop(0)
                        arm.state = shimon.arm.ArmState.STARTING
                        # Reset wait time
                        arm.waittime = 35
                        goto .fsmstart
                    else:
                        deceleration = -arm.direction * arm.deceleration()
                        newspeed = arm.speed + deceleration
                        newposition = arm.position + arm.speed + 0.5 * deceleration
                        # If we have reached past zero velocity in this cycle, wait for next message
                        if newspeed * arm.direction < -sys.float_info.epsilon:
                            arm.position = arm.currentinstructiontargetposition()
                            arm.speed = 0.0
                            arm.instructionqueue.pop(0)
                            arm.state = shimon.arm.ArmState.WAITING
                            print(f'Arm {arm.number} shifts to WAITING state at time {time - offset}', file=info)
                            arm.waittime = 35
                        arm.position = newposition
                        arm.speed = newspeed
                        # If we have reached past zero velocity after this cycle, wait for next message
                        if abs(arm.speed) < sys.float_info.epsilon:
                            arm.position = arm.currentinstructiontargetposition()
                            arm.speed = 0.0
                            arm.instructionqueue.pop(0)
                            arm.state = shimon.arm.ArmState.WAITING
                            print(f'Arm {arm.number} shifts to WAITING state at time {time - offset}', file=info)
                            arm.waittime = 35
                # if len(arm.instructionqueue) > 0: # and arm.number == 4:
                #     arm.reportlog(log)
        # log.write('\n')
        if arms[1].position - arms[0].position < 15.0:
            logerror(f'Arm 1 collides with arm 2 at {time - offset} ms')
            return False, [1, 2]
        elif arms[2].position - arms[1].position < 55.5:
            logerror(f'Arm 2 collides with arm 3 at {time - offset} ms')
            return False, [2, 3]
        elif arms[3].position - arms[2].position < 15.0:
            logerror(f'Arm 3 collides with arm 4 at {time - offset} ms')
            return False, [3, 4]
        elif arms[0].position < shimon.arm.positiontable[0]:
            logerror(f'Arm 1 moves beyond the rail at {time - offset} ms')
            return False, [1]
        elif arms[3].position > shimon.arm.positiontable[-1]:
            logerror(f'Arm 4 moves beyond the rail at {time - offset} ms')
            return False, [4]

        # Strikers
        if strikercommands is not None and len(strikercommands) > 0:
            for item in strikerhits.copy():
                if time >= item[1] + 200:
                    strikerhits.remove(item)
            for striker in strikers:
                if len(striker.instructionqueue) > 0:
                    # Hit the key when receiving the command after 85 ms
                    if time == striker.instructionqueue[0] + 85:
                        if not striker.isdead:
                            # Reset the counter
                            if (striker.lasthittime == -1):
                                striker.lasthittime = time
                                striker.deadcounter = 1
                            else:
                                # If the striker receives 3 or more messages at a rate of 13 hits per second or faster, it will die
                                if time - striker.lasthittime - math.ceil(1000 / parameters.strikermaxhitfrequency) <= sys.float_info.epsilon and time - striker.lasthittime >= sys.float_info.epsilon:
                                    striker.lasthittime = time
                                    striker.deadcounter += 1
                                    if striker.deadcounter == 3:
                                        striker.isdead = True
                                        loginfo(f'Striker {striker.number} is dead at time {time - offset}')
                                # Otherwise reset the counter
                                else:
                                    striker.lasthittime = time
                                    striker.deadcounter = 1
                            if not striker.isdead:
                                strikerhits.append((striker.number, time))
                                loginfo(f'Striker {striker.number} hits the keyboard at time {time - offset} on note {checkmidi.getnote(arms[striker.armnumber - 1].position)}')
                                hitnotes.append(checkmidi.getnote(arms[striker.armnumber - 1].position))
                        striker.instructionqueue.pop(0)
                        # Check note
                        if midifilename is not None:
                            if len(notelist) == 0:
                                if not striker.isdead:
                                    loginfo(f'Striker {striker.number} hits a note not in the MIDI file')
                            else:
                                # Skip whole chord when time get past the chord (e.g. the chord has 5 or more notes while Shimon's pathplanner can only choose 4)
                                if time - offset > max(notelist[0][0][0]) + parameters.timingthreshold:
                                    logwarning(f'Skipped MIDI notes {[item[1] for item in notelist[0]]} at time {notelist[0][0][0][0]}')
                                    notelist.pop(0)
                                isvalid, matchednote = checkmidi.isnotevalid(time - offset, checkmidi.getnote(arms[striker.armnumber - 1].position), notelist[0], parameters.timingthreshold)
                                if not isvalid:
                                    if not striker.isdead:
                                        logwarning(f'Striker hits a note {matchednote[0]} of correct pitch but different octave' if len(matchednote) > 0 else f'Striker {striker.number} hits a wrong note ({checkmidi.getnote(arms[striker.armnumber - 1].position)}) or at a wrong time ({time - offset}) compared to the MIDI file: {notelist[0]}')
                                else:
                                    notelist[0].remove(matchednote)
                                    if len(notelist[0]) == 0:
                                        notelist.pop(0)
    return True, hitnotes
