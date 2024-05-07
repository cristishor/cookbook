import crud_ops
import os
from sys import stdout
from utils import getWindowSize
from math import floor

global ENTRIES
global LAST_COMMAND
global ERR_FLAG

global COLS, LINES
global N_RENDERED_LINES

# CONSTANTS
NEW_LINE_SZ = 1

COMMANDS = {
    'entries': {
        'caca':'da'
    }
}



def cbinit():
    global ENTRIES
    global LAST_COMMAND
    global ERR_FLAG

    global COLS, LINES
    global N_RENDERED_LINES

    COLS, LINES = getWindowSize()
    ENTRIES = crud_ops.READ_ENTRIES()

    # init some other stacks if needed

    N_RENDERED_LINES = renderEntries()
    
    LAST_COMMAND = 'entries'
    ERR_FLAG = 0

def renderEntries(fields = None, filter = None):
    # fields: None (default)               - we only display names
    #         'all'                        - we display all fields
    #         ['field_1', 'field_2', ... ] - we display the specified fields   
    #
    # filter: None (default)   - we return all items
    #         'substring'      - we return all items with names that include the 'substring' string
    #         ['', '*date*']   - ...

    global ENTRIES
    global COLS, LINES
    
    os.system('cls')
    COLS, LINES = getWindowSize()

    items    = {}
    filtered = []

    if not filter:
        items = ENTRIES
    
    if not fields:
        filtered = list(items.keys())

    n_rows = 0
    for item in filtered:
        n_rows += len(item) / COLS + 1
        print(item)

    print()
    return n_rows

        


def handleInput(_input):
    # break down the input 
    input_tokens = _input.split(' ')
    available_commands = COMMANDS[LAST_COMMAND]

    if input_tokens[0] not in available_commands.keys():
        whoopsie = {'err_name':'BAD_COMMAND_TYPE', 'args':[input_tokens[0]]}
        return None, whoopsie
    else:
        print('bv')


def dispFailedAttempt(error, args):
    global ERR_FLAG
    
    match error:
        case 'BAD_COMMAND_TYPE':
            msg = f'Invalid command - cannot use "{args[0]}" for a "{LAST_COMMAND}" type menu.'
            ERR_FLAG = floor(len(msg) / COLS) + 1 + NEW_LINE_SZ

    print(f'Failed attempt {error}: {msg}\n')
    

def main():

    cbinit()
    global ERR_FLAG

    while True:

        user_input = input('> ')
        # clear the input
        stdout.write("\033[F")
        stdout.write("\033[K")

        if user_input == 'q' or user_input == 'Q':
            os.system('cls')
            break

        instructions, err = handleInput(user_input)

        if err:
            if ERR_FLAG:
                stdout.write("\033[F" * ERR_FLAG)
                stdout.write("\033[K" * ERR_FLAG)
            dispFailedAttempt(err['err_name'], err['args'])
            continue

        #some_object, render_type = execute_instructions(instructions)




if __name__ == '__main__':
    main()