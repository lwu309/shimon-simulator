import builtins
import sys

infofile = None
warningfile = None

def open(infofilename, warningfilename):
    global infofile
    global warningfile

    if infofilename is not None:
        infofile = builtins.open(infofilename, mode='w', encoding='utf-8')
    if warningfilename is not None:
        warningfile = builtins.open(warningfilename, mode='w', encoding='utf-8')

def close():
    global infofile
    global warningfile

    if infofile is not None:
        infofile.close()
        infofile = None
    if warningfile is not None:
        warningfile.close()
        warningfile = None

def info(message, echo=True):
    if echo:
        print(message, file=sys.stderr)
    if infofile is not None:
        print(message, file=infofile)

def warning(message, echo=True):
    message = 'Warning: ' + message
    if echo:
        print(message, file=sys.stderr)
    if infofile is not None:
        print(message, file=infofile)
    if warningfile is not None:
        print(message, file=warningfile)

def error(message, echo=True):
    message = 'Error: ' + message
    if echo:
        print(message, file=sys.stderr)
    if infofile is not None:
        print(message, file=infofile)
    if warningfile is not None:
        print(message, file=warningfile)
