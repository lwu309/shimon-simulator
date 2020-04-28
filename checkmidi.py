import mido
import sys

from shimon.arm import positiontable
import log

blackpositiontable = []
whitepositiontable = []
for i in range(4):
    for j in range(12):
        if j in [1, 3, 6, 8, 10]:
            blackpositiontable.append(positiontable[i * 12 + j])
        else:
            whitepositiontable.append(positiontable[i * 12 + j])

midimapping = {}
for i in range(48):
    midimapping[positiontable[i]] = i + 48

def findstaticoffset(time, notelist):
    return time - notelist[0][0][0][0]

def getnote(position, isblack):
    checkpositiontable = blackpositiontable if isblack else whitepositiontable
    if position in checkpositiontable:
        return midimapping[position]
    else:
        for i in range(len(checkpositiontable) - 1):
            if position > checkpositiontable[i] and position < checkpositiontable[i + 1]:
                if position - checkpositiontable[i] < checkpositiontable[i + 1] - position:
                    return midimapping[checkpositiontable[i]]
                else:
                    return midimapping[checkpositiontable[i + 1]]
        return None

def issamepitch(note1, note2):
    return abs(note1 - note2) % 12 == 0

def timingwindow(time, errorallowed):
    window = {time}
    for i in range(1, errorallowed + 1):
        window.add(time + i)
        window.add(time - i)
    return window

def isintimingwindow(window, checknote):
    for t in window:
        if t in checknote[0]:
            return True
    return False

def isnotevalid(time, note, checknotelist, errorallowed):
    reason = []
    if len(checknotelist) == 0:
        return False, reason
    window = timingwindow(time, errorallowed)
    if not isintimingwindow(window, checknotelist[0]):
        return False, reason
    for checknote in checknotelist:
        intimingwindow = isintimingwindow(window, checknote)
        if intimingwindow and note == checknote[1]:
            return True, checknote
        elif intimingwindow and issamepitch(note, checknote[1]):
            reason.append(checknote)
    return False, reason

def readnotes(filename):
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
            log.info(f'The tempo has been changed to {mido.tempo2bpm(message.tempo)} beats per minute, which is {message.tempo / midifile.ticks_per_beat} µs per tick')
        elif message.type == 'note_on':
            # We are in a chord when message time is zero
            if int(round(time * 1000, 4)) == currentchordtime and len(currentchord) != 0:
                if message.note >= 48 and message.note <= 95:
                    currentchord.append((currentchordtime, message.note))
                else:
                    log.warning(f'Midi note {message.note} at time {int(round(time * 1000, 4))} is out of range and will not be played by Shimon')
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
                    log.warning(f'Midi note {message.note} at time {int(round(time * 1000, 4))} is out of range and will not be played by Shimon')
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
