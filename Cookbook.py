# ENVIRONMENT GLOBAL VARIABLES
DB_FILE_NAME = 'test001.db'

# GLOBAL DEBUG FLAGS
TEST_SIMULATION = 0 # doesn't save the changes to the big DICT object to the DB
PRINT_DETOKENIZED_DATA_AT_READ = 0
PRINT_NEW_OR_EDITED_ENTRY = 1


### FETCH_DATA_FROM_DB method
def fetchDataFromDB(dbName = DB_FILE_NAME):

    def getDataFromDB(dbName):
        with open(dbName, "r") as f:
            ENTRIES = []
            if PRINT_DETOKENIZED_DATA_AT_READ: print()
            for line in f:
                entryName, history = detokenize(line)
                ENTRIES[entryName] = history
                if PRINT_DETOKENIZED_DATA_AT_READ:
                    print(entryName, '-', ENTRIES[entryName])
            if PRINT_DETOKENIZED_DATA_AT_READ: print()
            return ENTRIES

    def detokenize(line):
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
    
    return getDataFromDB(dbName)
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def sendNewOrEditedDataToDB(ENTRIES, entryName, newDate = None, dbName = DB_FILE_NAME ):
    def addLineToFile(line, dbName):
        with open(dbName, "a") as f:
            if (not line.endswith('\n')): 
                line = line.strip() + '\n'
            f.write(line)

    def addNewRecipeToDB(entryName, dbName, date = None ):
        if(date):
            entryName = entryName + '{' + str(date['d']) + '/' + str(date['m']) + '/' + str(date['y']) + '}'
        else:
            entryName =  entryName + '{}'
        addLineToFile(entryName, dbName)

    # NEW RECIPE
    if entryName not in ENTRIES:
        ENTRIES[entryName] = newDate
        if not TEST_SIMULATION:
            addNewRecipeToDB(entryName, dbName, newDate)

        if PRINT_NEW_OR_EDITED_ENTRY: print('\n', entryName, '-', newDate)
        return 'New recipe added successfully!'
    
    # NEW ENTRY
    elif newDate is not None:
        currEntry = ENTRIES[entryName]

        if PRINT_NEW_OR_EDITED_ENTRY: print('\nOLD:', entryName, '-', currEntry)
        if newDate in currEntry:
            return 'Warning: the chosen date already appears in the records!'
        
        lastItemFlag = 1
        for index, date in enumerate(currEntry):
            # TO DO: rethink the logic from here -> looks gnarly
            if date['y'] > newDate['y']:
                continue
            if date['m'] > newDate['m'] and date['y'] == newDate['y']:
                continue
            if date['d'] > newDate['d'] and date['m'] == newDate['m'] and date['y'] == newDate['y']:
                continue
            currEntry.insert(index, newDate)
            lastItemFlag = 0
            break
        if lastItemFlag:
            currEntry.append(newDate)
        if not TEST_SIMULATION: rewriteLine(entryName, currEntry, dbName) # TO DO: move the condition in the func
        if PRINT_NEW_OR_EDITED_ENTRY: print('NEW:', entryName, '-', currEntry)
        return 'New entry added successfully!'
    
    # old recipe, no new entry
    else:
        if PRINT_NEW_OR_EDITED_ENTRY: print('\nOLD:', entryName, '-', ENTRIES[entryName])
        return 'Warning: date not provided to append to the existing recipe!' 



def rewriteLine(entryName, history, dbName):
    newLine = tokenize(entryName, history)
    
    # FANCY (maybe) TO DO: do this w/o loading everything into the memory
    # nor by copying contents to a temp file
    with open(dbName, 'r') as f:
        lines = f.readlines()
    with open(dbName, 'w') as f:
        for line in lines:
            if entryName in line:
                f.write(newLine + '\n')
            else:
                f.write(line)
def tokenize(entryName, history):
    newLine = entryName
    if history == None:
        newLine = newLine + '{}'
    else:
        for date in history:
            newLine = newLine +'{' + str(date['d']) + '/' + str(date['m']) + '/' + str(date['y']) + '}'
        return newLine
    


def editOrDeleteRecipeDate(ENTRIES, entryName, oldDate, newDate = None):
    # (1) check whether desired newDate is valid
    history = ENTRIES[entryName]
    if oldDate not in history:
        return 'Fatal error: trying to access an entry (date) non existent to this recipe'
    if newDate != None and newDate in history:
        return 'Error: the chosen date already appears in the records!'
    history = deleteTargetDate(history, oldDate)
    sendNewOrEditedDataToDB(ENTRIES, entryName, newDate)
    if newDate == None:
        if PRINT_NEW_OR_EDITED_ENTRY: print('\nNEW:', entryName, '-', history)
        return 'Entry deleted successfully!'
    return 'Entry modified successfully!'
def deleteTargetDate(history, targetDate):
    for date in history:
        if date == targetDate:
            return [date for date in history if date != targetDate]
    


ENTRIES = fetchDataFromDB()
name = 'food_multiple_entries_1'
#newDate = {'d':6,'m':9,'y':2021}
#oldDate = {'d':2,'m':2,'y':2027}
oldDate = {'d':2,'m':2,'y':2023}
print(editOrDeleteRecipeDate(ENTRIES, name, oldDate))


# 4 big commands -> READ (an entry)
#                   ADD (entry OR date)
#                   EDIT (entryName OR date)
#                   DELETE (entry or date)
# -> Update the debug system/flags
# -> Update the writeline -> use FP
# -> Rename/reuse/rewire methods

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
