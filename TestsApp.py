import Cookbook

### GLOBAL ENV VAR
TEST_DB_1 = 'test001.db'

def test_Fetch_Data_From_DB():
    Cookbook.PRINT_DETOKENIZED_DATA_AT_READ = 1
    Cookbook.fetchDataFromDB(TEST_DB_1)

# RUN TESTS
test_Fetch_Data_From_DB()