"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package
from . import recipes
from . import db                        # import from local package

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    reader = parse_csv(fp)

    x = []
    n = 0
    for line in reader:
       try:
           (mfg, name, typ) = line
       except ValueError: 
            print 'badly formatted line: %s' % line
            continue
       n += 1
       db.add_bottle_type(mfg, name, typ)

    return n
 

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    reader = parse_csv(fp)

    x = []
    n = 0

    for line in reader:
	try: 
	    (mfg, name, amount) = line
	except ValueError:
	    print 'badly formatted line: %s' % line
	    continue

        n += 1
        db.add_to_inventory(mfg, name, amount)

    return n

def load_recipes(fp):

    reader = parse_csv(fp)
    n = 0
    for line in reader:
        name = line[0]
        ing = []
	#every other - pairs
        for i in range(1, len(line), 2):
            ing.append( (line[i], line[i+1]) )

        n+=1
	#print 'NAME: ', name
	#print 'INGREDIENTS: ' , ing 
        
	rec = name,ing
        #print 'rec:  ' , rec
	r = recipes.Recipe(rec[0],rec[1])
	#print 'RECIPE NAME: ' , r.name
	#print 'RECIPE ING: ' , r.ingredients
        db.add_recipe(r)

    return n

    
     

def parse_csv(fp):

    reader = csv.reader(fp)

    for line in reader:
        if not line or not line[0].strip() or line[0].startswith('#'):
            continue

        yield line
     

