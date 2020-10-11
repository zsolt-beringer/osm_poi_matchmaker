# -*- coding: utf-8 -*-

try:
    import traceback
    import logging
    import sys
    import re
except ImportError as err:
    logging.error('Error {error} import module: {module}', module=__name__, error=err)
    logging.error(traceback.print_exc())
    sys.exit(128)

def compare_strings(string1, string2 = ''):
    # New string
    if (string1 is '' or string1 is None) and (string2 is not '' and string2 is not None):
        return 'N'
    # Deleted string
    elif (string1 is not '' and string1 is not None) and (string2 is '' or string2 is None):
        return 'D'
    # Modified string
    elif  str(string1) != str(string2):
        return 'M'
    # Equal string
    elif str(string1) == str(string2):
        return 'E'
