"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    try:
        reader = csv.reader(fp)

        x = []
        n = 0
        for line in reader:
	    if not line[n].strip():
	        continue

            if line[0].startswith('#'):
               continue
        
            (mfg, name, typ) = line
            n += 1
            db.add_bottle_type(mfg, name, typ)

        return n
    except RuntimeError:
	print "There is a problem"


def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    try:
        reader = data_reader(fp)

        x = []
        n = 0
        for (mfg, name, amount) in reader:
            n += 1
            db.add_to_inventory(mfg, name, amount)

        return n
    except RuntimeError:
	print "There is a problem"
    
     

def data_reader(fp):

    reader = csv.reader(fp)
    x = []
    n = 0
    j = 0

    for line in reader:
        if not line[0].startswith('#'):
            x.append(line)

        elif line[n].split():
            x.append(line)

        n += 1

    # trying to get this part to work (didn't start project until 9pm)
    while j < len(x):
        yield x[j]
        j += 1
