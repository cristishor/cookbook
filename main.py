import crud_ops, static
import os
from sys import stdout
from math import floor


# __classes__
class handleAppState:
    def __init__(self, _COMMANDS):
        self.COMMANDS = _COMMANDS

        self.cmdErrName = ''
        self.cmdErrArgs = []

    def clearErr(self):
        self.cmdErrName = ''
        self.cmdErrArgs = []

class handleWindow:
    def __init__(self):
        self.winCols = 0
        self.winLines = 0        
        self.nStaticRenderedLines = 0
        self.nDynamicRenderedLines = 0
        self.newLineSize = 1
        self.getWindowSize()

    def getWindowSize(self):
        try:
            self.winCols, self.winLines = os.get_terminal_size(0)
        except OSError:
            self.winCols, self.winLines = os.get_terminal_size()
        return self.winCols, self.winLines
    
    def getStaticMenuLinesSize():
        pass

# ---------------------------------------- #

# __globals__
ENTRIES = {}

hAppState = None
hWindow   = None

def renderEntriesNames():
    os.system('cls')
    hWindow.getWindowSize()

    n_lines = 0
    for entry in ENTRIES:
        n_lines += floor(len(entry) / hWindow.winCols) + 1
        print(entry)
    print()

    hWindow.nDynamicRenderedLines = n_lines
    hWindow.nStaticRenderedLines = 0


def handleInput(_input):
    # break down the input 
    input_tokens = _input.split(' ')

    if input_tokens[0] not in hAppState.COMMANDS.keys():
        hAppState.cmdErrName = static.ERRS[0]
        hAppState.cmdErrArgs = [input_tokens[0]]
        return -1
    else:
        print('bv')

def getInput():
    user_input = input('> ')
    stdout.write("\033[F")
    stdout.write("\033[K")
    return user_input.lower()

def dispCommandError():
    error = hAppState.cmdErrName
    args  = hAppState.cmdErrArgs
    
    nRenderedLines = hWindow.nDynamicRenderedLines if hWindow.nDynamicRenderedLines else hWindow.nStaticRenderedLines
    winLines = hWindow.winLines
    winCols  = hWindow.winCols

    NEW_LINE_SZ = hWindow.newLineSize

    match error:
        case 'BAD_COMMAND_TYPE':
            msg = f'Invalid command "{args[0]}".'

        case _: 
            raise ('UNKNOW ERR - APPEND TO FUNCTION')
    
    err_sz = floor(len(msg) / winCols)+1 + NEW_LINE_SZ

    if nRenderedLines >= winLines:
        empty_lines = 2 * NEW_LINE_SZ
    else:
        empty_lines = winLines - nRenderedLines - err_sz

    for _ in range(empty_lines):
        print()

    stdout.write("\033[K")
    print(f'Failed attempt {error}: {msg}', end='')

    stdout.write("\033[F" * (empty_lines))

def main():

    # __init__
    global hAppState, hWindow, ENTRIES
    hAppState = handleAppState(static.COMMANDS) 
    hWindow   = handleWindow()
    ENTRIES = crud_ops.READ_ENTRIES()
        # TO DO: do the recomm algo
    renderEntriesNames()

    # __main loop__
    while True:

        user_input = getInput()
        if user_input == 'q' or user_input == 'quit':
            break

        rf = handleInput(user_input)
        if rf == -1:
            dispCommandError()
            continue

        # render
    
    # __deinit__
    os.system('cls')

        




if __name__ == '__main__':
    main()