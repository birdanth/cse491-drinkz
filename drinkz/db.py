"""
Database functionality for drinkz information.
"""

# private singleton variables at module level

_bottle_types_db = set([])  
_inventory_db = {}
_recipes_db = {}


def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set([])
    _inventory_db = {}
    _recipes_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    repeatFlag = False
    # if the bottle type already exists add the amounts together and associate
    # the sum to the same key (stored in ml)
    # Basically, when adding more of a type of liquor to the inventory
    # it keeps track of the total in ml automatically
    for k,v in _inventory_db.items():
	if k[0] == mfg and k[1] == liquor: 
	    currentValue =  v

	#this needs to change
            total = 0.0
	    currentDigit,ml = currentValue.split()
	    currentDigit = float(currentDigit)
	    total += currentDigit

            num, units = amount.split()
            num = float(num)
            units = units.lower()

            if units == 'ml':
                total += num
            elif units == 'oz':
                total += 29.5735 * num
	    elif units == 'gallons' or units == 'gallon' or units == 'gall':
		total += 3785.41 * num
            else:
                print "unknown unit type, not added to total"

	    newValue =  str(total) + ' ml'
            _inventory_db[(mfg, liquor)] = newValue
	    repeatFlag = True

    if not repeatFlag:
        _inventory_db[(mfg, liquor)] = amount


def convert_to_ml(amount):
    num, units = amount.split()
    num = float(num)
    units = units.lower()
    
    if units == 'ml':
        pass
    elif units == 'liters' || 'liter':
	num = 1000.0 * num
    elif units == 'oz':
        num = 29.5735 * num
    elif units == 'gallons' or units == 'gallon' or units == 'gall':
        num = 3785.41 * num
    else:
        print "unknown unit type, not added to total"
 
    return num

def check_inventory(mfg, liquor):
    for key  in _inventory_db:
        if key[0] == mfg and key[1] == liquor:
            return True
        
    return False


#To fix this and make it sum in both OZ and ML, but report in ML, amount could be 
#specified as a tuple of value and units, but it would only return the amount, after
#converting if need be, in ML.
def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    for k,v in _inventory_db.items():
        if k[0] == mfg and k[1] == liquor:
            amounts.append(v)

    total = 0.0
    for amount in amounts:
	#print "this is the amount: " , amount
	# amount is going ot be in format "number unit"
	num, units = amount.split()
	num = float(num)
	units = units.lower()

	if units == 'ml':
	    total += num
	elif units == 'oz':
	    total += 29.5735 * num
        elif units == 'gallons' or units == 'gallon' or units == 'gall':
            total += 3785.41 * num
	else:
	    raise Exception("unknown unit %s" % units)

    return  total

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        yield key

def add_recipe(r):
    # still need to check if a duplicate s added.
    _recipes_db[r.name] = r

def get_recipe(name):
    for k,v in _recipes_db.items():
	if k == name:
	    return k,v

def get_all_recipes():
    for k,v in _recipes_db.items():
	print "RECIPES:   " , (k,v)
	yield v
	#return _recipes_db.values()

def check_inventory_for_type(generic_type):
    mathching_ml = []
    for (m,l,t) in _bottle_types_db:
	if t == generic_type:
	    amount = _inventory_db.get((m,l),0.0)
	    matching_ml.append((m,l,amount))

    return matching_ml

