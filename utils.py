from typing import Dict

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
    'VALIDATE_DATE_DICT_TYPE',
    'VALIDATE_W_TYPE']