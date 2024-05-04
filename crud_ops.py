from utils import VALIDATE_DATE_DICT_TYPE, VALIDATE_W_TYPE

DEFAULT_W = 10
# ENVIRONMENT GLOBAL VARIABLES
DB_FILE_NAME = 'test001.db'

# GLOBAL DEBUG FLAGS
_TEST_SIMULATION = 0 # doesn't save the changes to the big DICT object to the DB

_PRINT_CRUD_OP = 1

_DEBUG_READ_DATA = 1
_DEBUG_CREATE_DATA = 1
_DEBUG_UPDATE_DATA = 0
_DEBUG_DELETE_DATA = 0


# ~ READ ENTRIES ~
def READ_ENTRIES(dbName = DB_FILE_NAME):

    if _PRINT_CRUD_OP: print('\nREAD_ENTRIES call:')

    with open(dbName, "r") as f:
        ENTRIES = {}
        if _DEBUG_READ_DATA: print()
        for line in f:
            entryName, fields = detokenizer(line)
            parse(entryName, fields, ENTRIES)

            if _DEBUG_READ_DATA:
                print(entryName, '- history:', ENTRIES[entryName]['history'], '- w:', ENTRIES[entryName]['weight'])

        return ENTRIES

# ~ READ ENTRY ~
def READ_ENTRY(ENTRIES, entryName, dbName = DB_FILE_NAME):
    if entryName not in ENTRIES:
        return 'Error: bad entry name!'
    entryData = ENTRIES[entryName]
    return entryData

# ~ CREATE ENTRY ~
def CREATE_ENTRY(ENTRIES, entryName, entryData = None, dbName = DB_FILE_NAME):
    msg_return_list = [
        ' > New entry added successfully!',
        ' > Error: the entry name already appears in the records!'
    ]

    if _PRINT_CRUD_OP: print('\nCREATE_ENTRY call:')

    if entryName not in ENTRIES:
        ENTRIES[entryName] = entryData
        if not _TEST_SIMULATION:
            newLine = tokenizer(entryName, entryData)
            addLineToFile(newLine, dbName)

        if _DEBUG_CREATE_DATA: print('New entry added:\n', newLine)
        return msg_return_list[0]
    else:
        if _DEBUG_CREATE_DATA: print(msg_return_list[1])
        return msg_return_list[1]
    
# ~ CREATE ADD DATE ~
def CREATE_ADD_DATE(ENTRIES, entryName, date, dbName = DB_FILE_NAME):
    msg_return_list = [
        ' > Error: date already existing in history!',
        ' > New date entry added successfully!'
    ]

    if _PRINT_CRUD_OP: print('\nCREATE_ADD_DATE call:')

    VALIDATE_DATE_DICT_TYPE(date)

    history = ENTRIES[entryName]['history']

    if date in history:
        return msg_return_list[0]
    
    if _DEBUG_CREATE_DATA: print('OLD:', entryName, '-', history)

    lastItemFlag = 1
    for index, _date in enumerate(history):
        # TO DO: rethink the logic from here -> looks gnarly
        if _date['y'] > date['y']:
            continue
        if _date['m'] > date['m'] and _date['y'] == date['y']:
            continue
        if _date['d'] > date['d'] and _date['m'] == date['m'] and _date['y'] == date['y']:
            continue
        history.insert(index, date)
        lastItemFlag = 0
        break
    if lastItemFlag:
        history.append(date)

    if not _TEST_SIMULATION: 
        newLine = tokenizer(entryName, ENTRIES[entryName])
        rewriteLineInFile(newLine, entryName, dbName)

    if _DEBUG_CREATE_DATA: print('NEW:', entryName, '-', history)    
    return msg_return_list[1]
    
# ~ SET WEIGHT ~
def SET_W(ENTRIES, entryName, weight = None, dbName = DB_FILE_NAME):

    if _PRINT_CRUD_OP: print('\SET_W call:')

    if weight == None:
    # return to default
        ENTRIES[entryName]['weight'] = DEFAULT_W
    else:
        VALIDATE_W_TYPE(weight)
        ENTRIES[entryName]['weight'] = weight

    if not _TEST_SIMULATION: 
        newLine = tokenizer(entryName, ENTRIES[entryName])
        rewriteLineInFile(newLine, entryName, dbName)

# ~ DELETE ENTRY ~
def DELETE_ENTRY(ENTRIES, entryName, dbName = DB_FILE_NAME):
    msg_return_list = [
        ' > Error: Missing target entry for deletion!',
        ' > Entry deleted successfull!'
    ]    
    
    if _PRINT_CRUD_OP: print('\nDELETE_ENTRY call:')

    if entryName not in ENTRIES:
        return msg_return_list[0]

    ENTRIES.pop(entryName)
    if not _TEST_SIMULATION:
        rewriteLineInFile(None, entryName, dbName)

    return msg_return_list[1]
    
# ~ DELETE ENTRY DATE ~
def DELETE_DATE(ENTRIES, entryName, targetDate, dbName = DB_FILE_NAME):
    msg_return_list = [
        ' > Error: Target date missing for deletion!',
        ' > Date deletion successfull!'
    ] 

    if _PRINT_CRUD_OP: print('\nDELET_DATE call:')

    VALIDATE_DATE_DICT_TYPE(targetDate)

    history = ENTRIES[entryName]['history']

    if targetDate in history:
        if _DEBUG_DELETE_DATA: print('OLD:', entryName, '-', history)
        history.pop(history.index(targetDate))
        if _DEBUG_DELETE_DATA: print('NEW:', entryName, '-', history)

        if not _TEST_SIMULATION:
            newLine = tokenizer(entryName, ENTRIES[entryName])
            rewriteLineInFile(newLine, entryName, dbName)
    else:
        return msg_return_list[0]
    return msg_return_list[1]
        
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
def tokenizer(entryName, entryData):
    history = entryData['history']
    weight  = entryData['weight']
    
    newLine = entryName
    if history != None:
        newLine += ':history'
        for date in history:
            newLine += '{' + str(date['d']) + '/' + str(date['m']) + '/' + str(date['y']) + '}'
    if weight != None and weight != DEFAULT_W:
        newLine += ':weight{' + str(weight) + '}'

    return newLine
    
def detokenizer(line):
    def main(line):
        name_index = line.find(':')
        entryName = line[:name_index]

        line = line[name_index+1:]

        # break all fields into separate tokens
        tokens = []
        for i in range(line.count(':')):
            index = line.find(':')
            tokens.append(line[:index])
            line = line[index+1:]
        if(line != '' and line != '\n'): 
            # can happen if our line ends with a ':' character
            tokens.append(line)

        # SWITCH STATEMENT : for every variable in the db
        fields = {}
        for token in tokens:
            if token.count('history'):
                fields['history'] = get_history(token[len('history'):])

            if token.count('weight'):
                fields['weight'] = get_weight(token[len('weight'):])
            else:
                fields['weight'] = DEFAULT_W

        return entryName, fields

    def get_history(string):
        history = []
        nloop = string.count('}')
        for i in range(nloop): 
            start = string.find('{') + 1
            end = string.find('}')
            substring = string[start:end]
            string = string[end+1:]

            s1 = substring.find('/')
            s2 = substring.find('/', s1+1)
            d = int(substring[:s1])
            m = int(substring[s1+1:s2])
            y = int(substring[s2+1:])

            history.append({'d':d,'m':m,'y':y})
        return history

    def get_weight(string):
        weight = int(string[1:string.find('}')])
        return weight

    return main(line)

def parse(key, fields, dict_structure):
    ALL_FIELDS = [
        'history',
        'weight'
    ]

    entryData = {}

    for _key in fields.keys():
        entryData[_key] = fields[_key]
        ALL_FIELDS.remove(_key)

    for _key in ALL_FIELDS:
        entryData[_key] = None
    
    dict_structure[key] = entryData


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

ENTRIES = READ_ENTRIES()
entryData = {'history':[{'d':10,'m':10,'y':2002}],'weight':69}

### TO DO:
# (1) Add some input sanitization : if the date is not a valid one
#       (!) A very special task: create myself a calendar module
#
# (n-1) When reading the data from the DB, construct TWO stacks: most recent and second most recent entries
#       for each recipe. 
#       Maybe also do a mean, for every food, over the course of the last year, a coefficient of how much of that
#       certain food we have eaten -> might be useful
# (n) About the recommending system: what if we have gaps in in the journal 
