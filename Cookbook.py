# ENVIRONMENT GLOBAL VARIABLES
DB_FILE_NAME = 'test001.db'

# GLOBAL DEBUG FLAGS
PRINT_DETOKENIZED_DATA_AT_READ = 0 


### FETCH_DATA_FROM_DB method
def fetchDataFromDB(dbName = DB_FILE_NAME):

    def getDataFromDB(dbName):
        with open(dbName, "r") as f:
            entries = []
            if PRINT_DETOKENIZED_DATA_AT_READ: print()
            for line in f:
                entryObj = detokenize(line)
                entries.append(entryObj)
                if PRINT_DETOKENIZED_DATA_AT_READ:
                    print(entryObj)
            if PRINT_DETOKENIZED_DATA_AT_READ: print()
            return entries

    def detokenize(line):
        recordIndex = line.find('{')
        entryName = line[:recordIndex]
        entryObj = {entryName:None}

        # if the entry has no date recorded, return the object w/ name and index
        if(line.find('{}') != -1):
            return entryObj

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
        entryObj = {entryName:datesArray}
        return entryObj
    
    return getDataFromDB(dbName)
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def addLineToFile(line, dbName = DB_FILE_NAME):
    with open(dbName, "a") as f:
        if (not line.endswith('\n')): 
            line = line.strip() + '\n'
        f.write(line)

def addNewRecipeToDB(index, name, date = None, dbName = DB_FILE_NAME):
    if(date):
        name = str(index) + '.' + name + '{' + str(date['d']) + '/' + str(date['m']) + '/' + str(date['y']) + '}'
    else:
        name = str(index) + '.' + name + '{}'
    addLineToFile(name, dbName)


# by deafult it uses DB_FILE_NAME
food = 'food_name'
date = {'d':23,'m':4,'y':2024}

#addNewRecipeToDB(index, food, date)
