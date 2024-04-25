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

        food_date = [
            'new_food', {'d':1,'m':1,'y':2024},
            'food_multiple_entries_1', {'d':2,'m':2,'y':2023},
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
        Cookbook.PRINT_NEW_OR_EDITED_ENTRY = 0
        Cookbook.TEST_SIMULATION = 0
                

#### RUN TESTS ###
test_Fetch_Data_From_DB()
test_Create_New_Entry(1)