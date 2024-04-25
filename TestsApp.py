import Cookbook

### GLOBAL ENV VAR
TEST_DB_1 = 'test001.db'

def test_Fetch_Data_From_DB(doTest = 0):
    if doTest:
        # Init flags / variables
        Cookbook.PRINT_DETOKENIZED_DATA_AT_READ = 1
        # Call processes
        Cookbook.fetchDataFromDB(TEST_DB_1)
        # Deinit flags / variables
        Cookbook.PRINT_DETOKENIZED_DATA_AT_READ = 0

def test_Create_New_Entry(doTest = 0):
    if doTest:
        # Init flags / variables
        Cookbook.PRINT_NEW_OR_EDITED_ENTRY = 1
        Cookbook.TEST_SIMULATION = 1

        food, date = [], []
        food.append('food_multiple_entries_1')
        date.append({'d':2,'m':2,'y':2023})
        food.append('food_multiple_entries_2')
        date.append({'d':10,'m':9,'y':2023})
        food.append('food_multiple_entries_3')
        date.append({'d':15,'m':9,'y':2023})

        # Call processes
        ALL_RECIPES = Cookbook.fetchDataFromDB(TEST_DB_1)
        for i in range(3):
            msg = Cookbook.sendNewOrEditedDataToDB(ALL_RECIPES, food[i], date[i])
            print(msg)

        # Deinit flags / variables
        Cookbook.PRINT_NEW_OR_EDITED_ENTRY = 0
        Cookbook.TEST_SIMULATION = 0
                

#### RUN TESTS ###
test_Fetch_Data_From_DB()
test_Create_New_Entry(1)