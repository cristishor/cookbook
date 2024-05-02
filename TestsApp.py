import Cookbook

### GLOBAL ENV VAR
TEST_DB_1 = 'test001.db'

def test_READ(doTest = 0):
    if doTest:
        # Init flags / variables
        Cookbook._TEST_SIMULATION = 1
        Cookbook._PRINT_CRUD_OP = 1
        Cookbook._DEBUG_READ_DATA = 1

        # Call processes
        Cookbook.fetchDataFromDB(TEST_DB_1)

        # Deinit flags / variables
        Cookbook._TEST_SIMULATION = 0
        Cookbook._PRINT_CRUD_OP = 0
        Cookbook._DEBUG_READ_DATA = 0

def test_CREATE(doTest = 0):
    if doTest:
        # Init flags / variables
        Cookbook._TEST_SIMULATION = 1
        Cookbook._PRINT_CRUD_OP = 1
        Cookbook._DEBUG_CREATE_DATA = 1

        food_date = [
            'new_food', {'d':1,'m':1,'y':2024},
            'food_multiple_entries_1', {'d':2,'m':2,'y':2025},
            'food_multiple_entries_2', {'d':10,'m':9,'y':2023},
            'food_multiple_entries_3', {'d':15,'m':9,'y':2023},
            'already_existing_food', None,
            'already_existing_food', {'d':1,'m':1,'y':2024}
        ]

        # Call processes
        print('\n##### START TEST ######')
        ALL_RECIPES = Cookbook.fetchDataFromDB(TEST_DB_1)
        for i in range(0, len(food_date), 2):
            msg = Cookbook.sendNewOrEditedDataToDB(ALL_RECIPES, food_date[i], food_date[i+1])
            print(msg)

        # Deinit flags / variables
        Cookbook._TEST_SIMULATION = 0
        Cookbook._PRINT_CRUD_OP = 0
        Cookbook._DEBUG_CREATE_DATA = 0
                
def test_DELETE(doTest = 0):
    if doTest:
        # Init flags / variables
        Cookbook._TEST_SIMULATION = 1
        Cookbook._PRINT_CRUD_OP = 1
        Cookbook._DEBUG_DELETE_DATA = 1

        # Call processes


        # Deinit flags / variables
        Cookbook._TEST_SIMULATION = 0
        Cookbook._PRINT_CRUD_OP = 0
        Cookbook._DEBUG_DELETE_DATA = 0


#### RUN TESTS ###
test_READ()
test_CREATE()
test_DELETE()
