# ENVIRONMENT GLOBAL VARIABLES
DB_FILE_NAME = 'test001.db'

# GLOBAL DEBUG FLAGS
TEST_SIMULATION = 0
PRINT_DETOKENIZED_DATA_AT_READ = 0
PRINT_NEW_OR_EDITED_ENTRY = 0


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
        
        for index, dateRecord in enumerate(currRecipe):
            # TO DO: rethink the logic from here -> looks gnarly
            if dateRecord['y'] < newDate['y']:
                continue
            if dateRecord['m'] < newDate['m'] and dateRecord['y'] == newDate['y']:
                continue
            if dateRecord['d'] < newDate['d'] and dateRecord['m'] == newDate['m'] and dateRecord['y'] == newDate['y']:
                continue
            currRecipe.insert(index, newDate)
            break
        if not TEST_SIMULATION:
            # TO DO: add the new entry in the DB too
            pass

        if PRINT_NEW_OR_EDITED_ENTRY: print('NEW:', recipeName, '-', currRecipe)
        return 'New entry added successfully!'
    
    # old recipe, no new entry
    else:
        if PRINT_NEW_OR_EDITED_ENTRY: print('\nOLD:', recipeName, '-', ALL_RECIPES[recipeName])
        return 'Warning: date not provided to append to the existing recipe!' 





# ALL_RECIPES = fetchDataFromDB()

