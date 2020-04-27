import mido
import sys

import shimon.arm

midimapping = {}
for i in range(48):
    midimapping[shimon.arm.positiontable[i]] = i + 48

def findstaticoffset(time, notelist):
    return time - notelist[0][0][0][0]

def getnote(position):
    if position in shimon.arm.positiontable:
        return midimapping[position]
    else:
        for i in range(len(shimon.arm.positiontable) - 1):
            if position > shimon.arm.positiontable[i] and position < shimon.arm.positiontable[i + 1]:
                if position - shimon.arm.positiontable[i] < shimon.arm.positiontable[i + 1] - position:
                    return midimapping[shimon.arm.positiontable[i]]
                else:
                    return midimapping[shimon.arm.positiontable[i + 1]]
        return None

def isinoctave(note1, note2):
    return note1 > note2 - 12 and note1 < note2 + 12

def timingwindow(time, errorallowed):
    window = {time}
    for i in range(1, errorallowed + 1):
        window.add(time + i)
        window.add(time - i)
    return window

def isnotevalid(time, note, checknotelist, errorallowed):
    reason = []
    if len(checknotelist) == 0:
        return False, reason
    if time not in checknotelist[0][0] and time - 1 not in checknotelist[0][0] and time + 1 not in checknotelist[0][0]:
        return False, reason
    for checknote in checknotelist:
        intimingwindow = False
        for t in timingwindow(time, errorallowed):
            if t in checknote[0]:
                intimingwindow = True
                break
        if intimingwindow and isinoctave(note, checknote[1]):
            return True, checknote
        elif intimingwindow and abs(note - checknote[1]) % 12 == 0:
            reason.append(checknote)
    return False, reason

def readnotes(filename, info, warning):
    def logwarning(logmessage):
        logmessage = 'Warning: ' + logmessage
        print(logmessage, file=sys.stderr)
        print(logmessage, file=info)
        print(logmessage, file=warning)

    midifile = mido.MidiFile(filename)
    print('Ticks per beat:', midifile.ticks_per_beat)
    n = 0
    f = open('messages.txt', 'w')
    notesfile = open('notes.txt', 'w')
    time = 0
    notes = []
    currentchord = []
    currentchordtime = 0
    for message in midifile:
        time += message.time
        f.write(f'{message}\n')
        if message.type == 'set_tempo':
            print(f'The tempo has been changed to {mido.tempo2bpm(message.tempo)} beats per minute, which is {message.tempo / midifile.ticks_per_beat} µs per tick')
        elif message.type == 'note_on':
            # We are in a chord when message time is zero
            if int(round(time * 1000, 4)) == currentchordtime and len(currentchord) != 0:
                if message.note >= 48 and message.note <= 95:
                    currentchord.append((currentchordtime, message.note))
                else:
                    logwarning(f'Midi note {message.note} at time {int(round(time * 1000, 4))} is out of range and will not be played by Shimon')
            # Otherwise we are on the first note of the chord
            else:
                # Flush non-empty chord first
                if len(currentchord) != 0:
                    # Construct a range of timestamps
                    timestamps = []
                    for i in range(len(currentchord)):
                        timestamps.append(currentchordtime + i * 20)
                    # Overwrite chord with timestamp list
                    for i in range(len(currentchord)):
                        currentchord[i] = (timestamps, currentchord[i][1])
                    # Write chord
                    notesfile.write(f'{currentchord}\n')
                    notes.append(currentchord)
                    n += len(currentchord)
                    currentchord = []
                # Start a new chord
                if message.note >= 48 and message.note <= 95:
                    currentchord = [(int(round(time * 1000, 4)), message.note)]
                    currentchordtime = int(round(time * 1000, 4))
                else:
                    logwarning(f'Midi note {message.note} at time {int(round(time * 1000, 4))} is out of range and will not be played by Shimon')
    # Flush non-empty chord
    if len(currentchord) != 0:
        # Construct a range of timestamps
        timestamps = []
        for i in range(len(currentchord)):
            timestamps.append(currentchordtime + i * 20)
        # Overwrite chord with timestamp list
        for i in range(len(currentchord)):
            currentchord[i] = (timestamps, currentchord[i][1])
        # Write chord
        notesfile.write(f'{currentchord}\n')
        notes.append(currentchord)
        n += len(currentchord)
    notesfile.close()
    f.close()
    return n, notes

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please specify an input file name', file=sys.stderr)
    else:
        numberofnotes, _ = readnotes(sys.argv[1])
        print('The MIDI file has', numberofnotes, 'notes')
