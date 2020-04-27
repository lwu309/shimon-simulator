import platform
import time
import thirdparty.fluidsynth as fluidsynth

if platform.system() == 'Windows':
    fluidsynthdriver = 'dsound'
elif platform.system() == 'Darwin':
    fluidsynthdriver = 'coreaudio'
else:
    fluidsynthdriver = 'alsa'

fs = fluidsynth.Synth()
fs.start(fluidsynthdriver)

# https://musical-artifacts.com/artifacts/416
sfid = fs.sfload('marimba-deadstroke.sf2')
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 80)
fs.noteon(0, 67, 80)
fs.noteon(0, 76, 80)

time.sleep(1.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

time.sleep(1.0)

fs.delete()
