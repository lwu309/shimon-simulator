# SoundFont TimGM6mb from MuseScore
# Licensed in GPLv2
import os
import platform

# Include bin directory in path environment variable for Windows
if platform.system() == 'Windows':
    os.environ['PATH'] = os.getcwd() + os.sep + 'bin' + os.pathsep + os.environ['PATH']

import thirdparty.fluidsynth as fluidsynth

fs = None
sfid = -1

def start():
    global fs
    if platform.system() == 'Windows':
        fluidsynthdriver = 'dsound'
    elif platform.system() == 'Darwin':
        fluidsynthdriver = 'coreaudio'
    else:
        fluidsynthdriver = 'alsa' # Should work for most Linux systems, feel free to change

    fs = fluidsynth.Synth()
    fs.start(fluidsynthdriver)
    sfid = fs.sfload('sound/TimGM6mb.sf2')
    fs.program_select(0, sfid, 0, 13)

def play(note):
    global fs
    fs.noteon(0, note, 127)
