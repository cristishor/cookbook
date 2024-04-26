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
            entries = {}
            if PRINT_DETOKENIZED_DATA_AT_READ: print()
            for line in f:
                name, dates = detokenize(line)
                entries[name] = dates
                if PRINT_DETOKENIZED_DATA_AT_READ:
                    print(name, '-', entries[name])
            if PRINT_DETOKENIZED_DATA_AT_READ: print()
            return entries

    def detokenize(line):
        recordIndex = line.find('{')
        entryName = line[:recordIndex]

        # if the entry has no date recorded, return the object w/ name and index
        if(line.find('{}') != -1):
            return entryName, None

        date_index = 0
        datesArray = []
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

            datesArray.append({'d':d,'m':m,'y':y})

            date_index = next_date_index + 1
        return entryName, datesArray
    
    return getDataFromDB(dbName)
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def sendNewOrEditedDataToDB(ALL_RECIPES, recipeName, newDate = None, dbName = DB_FILE_NAME ):
    def addLineToFile(line, dbName):
        with open(dbName, "a") as f:
            if (not line.endswith('\n')): 
                line = line.strip() + '\n'
            f.write(line)

    def addNewRecipeToDB(name, dbName, date = None, ):
        if(date):
            name = name + '{' + str(date['d']) + '/' + str(date['m']) + '/' + str(date['y']) + '}'
        else:
            name =  name + '{}'
        addLineToFile(name, dbName)

    # NEW RECIPE
    if recipeName not in ALL_RECIPES:
        ALL_RECIPES[recipeName] = newDate
        if not TEST_SIMULATION:
            addNewRecipeToDB(recipeName, dbName, newDate)

        if PRINT_NEW_OR_EDITED_ENTRY: print('\n', recipeName, '-', newDate)
        return 'New recipe added successfully!'
    
    # NEW ENTRY
    elif newDate is not None:
        currRecipe = ALL_RECIPES[recipeName]

        if PRINT_NEW_OR_EDITED_ENTRY: print('\nOLD:', recipeName, '-', currRecipe)
        if newDate in currRecipe:
            return 'Warning: the chosen date already appears in the records!'
        
        lastItemFlag = 1
        for index, dateRecord in enumerate(currRecipe):
            # TO DO: rethink the logic from here -> looks gnarly
            if dateRecord['y'] > newDate['y']:
                continue
            if dateRecord['m'] > newDate['m'] and dateRecord['y'] == newDate['y']:
                continue
            if dateRecord['d'] > newDate['d'] and dateRecord['m'] == newDate['m'] and dateRecord['y'] == newDate['y']:
                continue
            currRecipe.insert(index, newDate)
            lastItemFlag = 0
            break
        if lastItemFlag:
            currRecipe.append(newDate)
        if not TEST_SIMULATION:
            rewriteLine(recipeName, currRecipe, dbName)
        if PRINT_NEW_OR_EDITED_ENTRY: print('NEW:', recipeName, '-', currRecipe)
        return 'New entry added successfully!'
    
    # old recipe, no new entry
    else:
        if PRINT_NEW_OR_EDITED_ENTRY: print('\nOLD:', recipeName, '-', ALL_RECIPES[recipeName])
        return 'Warning: date not provided to append to the existing recipe!' 



def rewriteLine(recipeName, datesArray, dbName):
    newLine = tokenize(recipeName, datesArray)
    
    # FANCY (maybe) TO DO: do this w/o loading everything into the memory
    # nor by copying contents to a temp file
    with open(dbName, 'r') as f:
        lines = f.readlines()
    with open(dbName, 'w') as f:
        for line in lines:
            if recipeName in line:
                f.write(newLine + '\n')
            else:
                f.write(line)
def tokenize(name, dateArray):
    newLine = name
    if dateArray == None:
        newLine = newLine + '{}'
    else:
        for date in dateArray:
            newLine = newLine +'{' + str(date['d']) + '/' + str(date['m']) + '/' + str(date['y']) + '}'
        return newLine
    


def editOrDeleteRecipeDate(ALL_RECIPES, recipeName, oldDate, newDate = None):
    # (1) check whether desired newDate is valid
    datesArray = ALL_RECIPES[recipeName]
    if oldDate not in datesArray:
        return 'Fatal error: trying to access an entry (date) non existent to this recipe'
    if newDate != None and newDate in datesArray:
        return 'Error: the chosen date already appears in the records!'
    datesArray = deleteTargetDate(datesArray, oldDate)
    sendNewOrEditedDataToDB(ALL_RECIPES, recipeName, newDate)
    if newDate == None:
        if PRINT_NEW_OR_EDITED_ENTRY: print('\nNEW:', recipeName, '-', datesArray)
        return 'Entry deleted successfully!'
    return 'Entry modified successfully!'
def deleteTargetDate(datesArray, targetDate):
    for date in datesArray:
        if date == targetDate:
            return [date for date in datesArray if date != targetDate]
    


ALL_RECIPES = fetchDataFromDB()
name = 'food_multiple_entries_1'
#newDate = {'d':6,'m':9,'y':2021}
#oldDate = {'d':2,'m':2,'y':2027}
oldDate = {'d':2,'m':2,'y':2023}
print(editOrDeleteRecipeDate(ALL_RECIPES, name, oldDate))

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
