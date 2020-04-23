import mido
import sys

epsilon = 0.00001
positiontable = [0, 10, 44, 73, 102, 157, 184, 212, 240, 267, 294, 324, 377, 406, 434, 463, 490, 546, 574, 599, 624, 651, 673, 698, 749, 771, 798, 820, 846, 894, 919, 945, 969, 993, 1018, 1044, 1092, 1118, 1142, 1167, 1193, 1240, 1266, 1291, 1315, 1339, 1364, 1385, 1385]

def readnotes(filename):
    midifile = mido.MidiFile(filename)
    print(midifile.ticks_per_beat)
    n = 0
    f = open('messages.txt', 'w')
    notesfile = open('notes.txt', 'w')
    time = 0
    for message in midifile:
        time += message.time
        f.write('{}\n'.format(str(message)))
        if message.type == "set_tempo":
            print("The tempo has been changed to {} beats per minute, which is".format(mido.tempo2bpm(message.tempo)), message.tempo / midifile.ticks_per_beat, "µs per tick")
        if message.type == "note_on":
            notesfile.write('({}, {})\n'.format(round(time * 1000, 4), positiontable[message.note - 48]))
            n += 1
    notesfile.close()
    f.close()
    return n

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify an input file name", file=sys.stderr)
    else:
        print("The MIDI file has", readnotes(sys.argv[1]), "notes")
