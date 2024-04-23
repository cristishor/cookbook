DB_FILE_NAME = 'cookbook.db'

def getDataFromDB(dbName = DB_FILE_NAME):
    with open(dbName, "r") as f:
        entries = []
        for line in f:
            entries.append(detokenize(line))
        return entries

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
        
def detokenize(line):
    dot_index = line.find('.')
    entryIndex = int(line[:dot_index])

    name_index = line.find('{')
    name = line[dot_index+1:name_index]
    entryObj = {'index':entryIndex, 'name':name}

    # if the entry has no date recorded, return the object w/ name and index
    if(line.find('{}') != -1):
        return entryObj

    entryObj.update({'dates':[]})
    date_index = 0
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

        entryObj['dates'].append({'d':d,'m':m,'y':y})

        date_index = next_date_index + 1
    
    return entryObj

        
# by deafult it uses DB_FILE_NAME
food = 'food_name'
date = {'d':23,'m':4,'y':2024}

index = 3
#addNewRecipeToDB(index, food, date)

print(getDataFromDB())


#Food1{1/1/1}{2/2/2}
#Food2{}

    