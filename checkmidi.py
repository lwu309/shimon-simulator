import mido
import sys

positiontable = [0, 10, 44, 73, 102, 157, 184, 212, 240, 267, 294, 324, 377, 406, 434, 463, 490, 546, 574, 599, 624, 651, 673, 698, 749, 771, 798, 820, 846, 894, 919, 945, 969, 993, 1018, 1044, 1092, 1118, 1142, 1167, 1193, 1240, 1266, 1291, 1315, 1339, 1364, 1385, 1385]

midimapping = {}
for i in range(48):
    midimapping[positiontable[i]] = i + 48

def findstaticoffset(time, notelist):
    return time - notelist[0][0][0][0]

def isnotevalid(time, note, checknotelist):
    if len(checknotelist) == 0:
        return False, None
    if time not in checknotelist[0][0]:
        return False, None
    for checknote in checknotelist:
        if time in checknote[0] and note == checknote[1]:
            return True, checknote
    return False, None

def roundposition(position):
    pass

def readnotes(filename):
    midifile = mido.MidiFile(filename)
    print(midifile.ticks_per_beat)
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
                    print(f'Midi note {message.note} at time {int(round(time * 1000, 4))} will not be played by Shimon', file=sys.stderr)
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
                # Start a new chord
                if message.note >= 48 and message.note <= 95:
                    currentchord = [(int(round(time * 1000, 4)), message.note)]
                    currentchordtime = int(round(time * 1000, 4))
                else:
                    print(f'Midi note {message.note} at time {int(round(time * 1000, 4))} will not be played by Shimon', file=sys.stderr)
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
