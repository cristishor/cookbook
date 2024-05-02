# ENVIRONMENT GLOBAL VARIABLES
DB_FILE_NAME = 'test001.db'

# GLOBAL DEBUG FLAGS
_TEST_SIMULATION = 0 # doesn't save the changes to the big DICT object to the DB

_PRINT_CRUD_OP = 0

_DEBUG_READ_DATA = 0
_DEBUG_CREATE_DATA = 0
_DEBUG_UPDATE_DATA = 0
_DEBUG_DELETE_DATA = 0


# ~ READ ENTRIES ~
def READ_ENTRIES(dbName = DB_FILE_NAME):

    if _PRINT_CRUD_OP: print('\nREAD_ENTRIES call:')

    with open(dbName, "r") as f:
        ENTRIES = {}
        if _DEBUG_READ_DATA: print()
        for line in f:
            entryName, history = detokenizer(line)
            ENTRIES[entryName] = history
            if _DEBUG_READ_DATA:
                print(entryName, '-', ENTRIES[entryName], '\n')
        return ENTRIES

# ~ READ ENTRY ~
def READ_ENTRY(ENTRIES, entryName, dbName = DB_FILE_NAME):
    if entryName not in ENTRIES:
        return 'Error: bad entry name!'
    history = ENTRIES[entryName]
    return history

# ~ CREATE ENTRY ~
def CREATE_ENTRY(ENTRIES, entryName, newDate = None, dbName = DB_FILE_NAME):
    msg_return_list = [
        ' > New entry added successfully!',
        ' > Warning: the chosen date already appears in the records!',
        ' > New date entry added successfully!',
        ' > Warning: date not provided to append to the existing recipe!'
    ]

    if _PRINT_CRUD_OP: print('\nCREATE_ENTRY call:')
    
    # 1 - NEW entry
    if entryName not in ENTRIES:
        ENTRIES[entryName] = newDate
        if not _TEST_SIMULATION:
            newLine = tokenizer(entryName, [newDate])
            addLineToFile(newLine, dbName)

        if _DEBUG_CREATE_DATA: print('New entry added:', entryName, '-', newDate, '\n', msg_return_list[0])

        return msg_return_list[0]
    
    # 2 - OLD entry, NEW date
    elif newDate is not None:
        currHistory = ENTRIES[entryName]

        if newDate in currHistory:
            return msg_return_list[1]
        
        if _DEBUG_CREATE_DATA: print('OLD:', entryName, '-', currHistory)

        lastItemFlag = 1
        for index, date in enumerate(currHistory):
            # TO DO: rethink the logic from here -> looks gnarly
            if date['y'] > newDate['y']:
                continue
            if date['m'] > newDate['m'] and date['y'] == newDate['y']:
                continue
            if date['d'] > newDate['d'] and date['m'] == newDate['m'] and date['y'] == newDate['y']:
                continue
            currHistory.insert(index, newDate)
            lastItemFlag = 0
            break
        if lastItemFlag:
            currHistory.append(newDate)

        if not _TEST_SIMULATION: 
            newLine = tokenizer(entryName, currHistory)
            rewriteLineInFile(newLine, entryName, dbName)

        if _DEBUG_CREATE_DATA: print('NEW:', entryName, '-', currHistory, '\n', msg_return_list[2])

        return msg_return_list[2]
    
    # 3 - OLD entry, NULL date
    else:
        if _DEBUG_CREATE_DATA: print('OLD:', entryName, '-', ENTRIES[entryName], '\n', msg_return_list[3])
        return msg_return_list[3]
    
# ~ DELETE ENTRY ~
def DELETE_ENTRY(ENTRIES, entryName, targetDate = None, dbName = DB_FILE_NAME):
    msg_return_list = [
        ' > Warning: Missing target date for deletion!',
        ' > Date deletion successfull!',
        ' > Entry deleted successfull!',
        ' > Error: Missing target entry for deletion!'
    ]    
    
    if _PRINT_CRUD_OP: print('\nDELETE ENTRY call:')

    # 1 - delete entry date
    if targetDate:
        history = ENTRIES[entryName]

        if _DEBUG_DELETE_DATA: print('OLD:', entryName, '-', history)

        if targetDate in history:
            history.pop(history.index(targetDate))

            if _DEBUG_DELETE_DATA: print('NEW:', entryName, '-', history)

            if not _TEST_SIMULATION:
                newLine = tokenizer(entryName, history)
                rewriteLineInFile(newLine, entryName, dbName)
        else:
            return msg_return_list[0]
        return msg_return_list[1]

    # 2 - delete entry completely 
    else:
        if entryName in ENTRIES:
            ENTRIES.pop(entryName)
            if not _TEST_SIMULATION:
                rewriteLineInFile(None, entryName, dbName)

            if _DEBUG_DELETE_DATA:
                for obj in ENTRIES:
                    print(obj)

            return msg_return_list[2]
        else:
            return msg_return_list[3]

# ~ UPDATE ENTRY HISTORY ~
def UPDATE_ENTRY(ENTRIES, entryName, targetDate = None, newDate = None, newEntryName = None, dbName = DB_FILE_NAME):
    msg_return_list = [
        ' > Error: Invalid target date for update!',
        ' > Error: Invalid new date already existent!',
        ' > Entry date updated successfull!!',
        ' > Error: Invalid syntax - missing targetDate / newDate!',
        ' > Entry name updated successfully!',
        ' > Error: Invalid syntax!',
    ]    

    if _PRINT_CRUD_OP: print('\nUPDATE ENTRY call:')

    # 1 - update entry date
    if targetDate and newDate:
        history = ENTRIES[entryName]

        if targetDate not in history:
            return msg_return_list[0]
        elif newDate in history:
            return msg_return_list[1]
        
        if _DEBUG_UPDATE_DATA: print('OLD:', entryName, '-', history)

        DELETE_ENTRY(ENTRIES, entryName, targetDate)
        CREATE_ENTRY(ENTRIES, entryName, newDate)

        if _DEBUG_UPDATE_DATA: print('NEW:', entryName, '-', ENTRIES[entryName])
        return msg_return_list[2]

    # 2 - bad request
    elif targetDate or newDate:
        return msg_return_list[3]

    # 3 - update entry name (no targetDate or newDate) 
    elif newEntryName:
        if newEntryName == entryName:
            return
        
        if _DEBUG_UPDATE_DATA: print('NEW:', entryName, '-', ENTRIES[entryName])
        
        ENTRIES[newEntryName] = ENTRIES.pop(entryName)
        if not _TEST_SIMULATION:
            newLine = tokenizer(newEntryName, ENTRIES[newEntryName])
            rewriteLineInFile(newLine, entryName, dbName)

        if _DEBUG_UPDATE_DATA: print('OLD:', newEntryName, '-', ENTRIES[newEntryName])
        return msg_return_list[4]

    # 4 - bad request
    else:
        return msg_return_list[5]


# @token
def tokenizer(entryName, history):
    newLine = entryName
    if history == None:
        newLine = newLine + '{}'
    else:
        for date in history:
            newLine = newLine +'{' + str(date['d']) + '/' + str(date['m']) + '/' + str(date['y']) + '}'
        return newLine
    
def detokenizer(line):
    name_index = line.find('{')
    entryName = line[:name_index]

    # if the entry has no date recorded, return the object w/ name and index
    if(line.find('{}') != -1):
        return entryName, None

    date_index = 0
    history = []
    while True:
        next_date_index = line.find('{', date_index)

        if next_date_index == -1: 
            break
        
        closing_bracket_index = line.find('}', next_date_index)
        date = line[next_date_index+1:closing_bracket_index]
        s1 = date.find('/')
        s2 = date.find('/', s1+1)
        d = int(date[:s1])
        m = int(date[s1+1:s2])
        y = int(date[s2+1:])

        history.append({'d':d,'m':m,'y':y})

        date_index = next_date_index + 1
    return entryName, history

# @file
def addLineToFile(line, dbName):
    with open(dbName, "a") as f:
        if (not line.endswith('\n')): 
            line = line.strip() + '\n'
        f.write(line)

def rewriteLineInFile(newLine, entryName, dbName):
    # ̵T̵O̵ ̵D̵O: do this w/o loading everything into the memory
    # nor by copying contents to a temp file
    # ... 
    # later edit: this is not possible due to python abstraction 
    # => TO DO: good oportunity to call some C functions from python :)
    with open(dbName, 'r') as f:
        lines = f.readlines()
    with open(dbName, 'w') as f:
        for line in lines:
            if entryName in line:
                if newLine != None:
                    f.write(newLine + '\n')
                else:
                    pass    # if newLine arg == None => line was deleted, do not write it
            else:
                f.write(line)


### TO DO:
# (1) Add some input sanitization : if newDate > todayDate => cant do;
#     or if the date is not a valid one <= (!) task
# (2) Refactor a bit the tokenize stuff -> using 2 diff functions for read and write from/to the db
#     !! use better / more uniform naming conventions !! 
# (3) Add an edit (+ delete) recipe/entry + extend tests
#
# ...
# (!) A very special task: create myself a calendar module
#
# (n-1) When reading the data from the DB, construct TWO stacks: most recent and second most recent entries
#       for each recipe. 
#       Maybe also do a mean, for every food, over the course of the last year, a coefficient of how much of that
#       certain food we have eaten -> might be useful
# (n) About the recommending system: what if we have gaps in in the journal 
