from typing import Dict
import os

CFG_FILE_PATH = '.\\config.txt'

# ~ IMPORT CFG FROM CONFIG FILE ~

def IMPORT_CFG(_file = CFG_FILE_PATH):
    settings = {}
    with open(_file) as f:
        for line in f:
            ind = line.find('=')
            key = line[:ind]
            value = line[ind+1:]
            settings[key] = value
    return settings

# ~ DB SYNC WITH GIT
# TO DO 


# ~ TERMINAL OPERATIONS ~
def getWindowSize():
    try:
        columns, lines = os.get_terminal_size(0)
    except OSError:
        columns, lines = os.get_terminal_size()
    return columns, lines


# ~ DATA VALIDATION ~

def VALIDATE_DATE_DICT_TYPE(_date: Dict[str, int]):
    required_keys = {'d', 'm', 'y'}
    if not all(key in _date for key in required_keys):
        raise TypeError("Missing required keys in data")
    
    if len(_date) != len(required_keys):
        raise TypeError("Extra keys found in data")
    
    if not all(isinstance(value, int) for value in _date.values()):
        raise TypeError("All values in data must be integers")
    
def VALIDATE_W_TYPE(_w: int):
    IS_INT(_w)

def IS_INT(_var: int):
    if not isinstance(_var, int):
        raise TypeError("Value must be an integer")


__all__ = [
    'IMPORT_CFG',

    'getWindowSize',

    'VALIDATE_DATE_DICT_TYPE',
    'VALIDATE_W_TYPE']


### MASSIVE TO DO LIST:
# (1) Add some input sanitization : if the date is not a valid one
#       (!) A very special task: create myself a calendar module
#
# (n-1) When reading the data from the DB, construct TWO stacks: most recent and second most recent entries
#       for each recipe. 
#       Maybe also do a mean, for every food, over the course of the last year, a coefficient of how much of that
#       certain food we have eaten -> might be useful
# (n) About the recommending system: what if we have gaps in in the journal 
#
# -- script some python to pull and commit/push changes at starting/closing the app
#    in order to save my personal cookbook db and keep it in sync with other devices 
