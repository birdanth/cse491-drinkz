
"""
Database functionality for drinkz information.
"""
from . import  unitconversion
from cPickle import dump, load
import sqlite3, os
import cPickle

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes = {}

try:
    os.unlink('tables.db')
except OSError:
    pass

db_conn = sqlite3.connect('tables.db')
c = db_conn.cursor()

# bottle types
c.execute("CREATE TABLE if not exists bottle_types ( mfg TEXT , lqr TEXT, typ TEXT )")

# inventory
c.execute("CREATE TABLE if not exists inventory ( mfg TEXT , lqr TEXT, amt INTEGER UNSIGNED DEFAULT '0' )")

# recipes
c.execute("CREATE TABLE if not exists recipes ( recipe TEXT )")

# recipe -> drink mapping
c.execute("CREATE TABLE if not exists pairings ( rec_name TEXT, drink_name TEXT )")

# add some sample mappings
c.execute("INSERT INTO pairings ( rec_name, drink_name) VALUES( 'Steak au Poivre', 'Beringer Cabernet 2006' )")  


db_conn.commit()
db_conn.close()


def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes = {}


def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipes)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipes
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipes) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass


def _reset_tables(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('DELETE FROM bottle_types')
    c.execute('DELETE FROM inventory')
    c.execute('DELETE FROM recipes')
    conn.commit()
    conn.close()



def print_contents(db_name):
    contents = []
    print_conn = sqlite3.connect(db_name)
    print_cursor = print_conn.cursor()
    print_cursor.execute("SELECT * from bottle_types")
    contents.append( " BOTTLE TYPES: ")
    contents.append( print_cursor.fetchall() )
    print_cursor.execute("SELECT * from inventory")
    contents.append( " INVENTORY: ")
    contents.append( print_cursor.fetchall() )
    contents.append( " RECIPES: ")
    print_cursor.execute("SELECT * from recipes")
    contents.append( print_cursor.fetchall() )
    print_conn.close()
    return contents


def get_pairings():
    contents = []
    print_conn = sqlite3.connect('tables.db')
    print_cursor = print_conn.cursor()
    print_cursor.execute("INSERT INTO pairings ( rec_name, drink_name) VALUES( 'Steak au Poivre', 'Beringer Cabernet 2006' )")  
    print_cursor.execute("SELECT * from pairings")
    contents.append( " PAIRINGS: ")
    contents.append( print_cursor.fetchall() )
    print_conn.close()
    return contents




def save_db_tables(db_name):

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for mfg,lqr,typ in _bottle_types_db:
        c.execute("INSERT INTO bottle_types (mfg,lqr,typ) VALUES (?,?,?) ", (mfg,lqr,typ) )

    for item in _inventory_db:
        (mfg, lqr) = item
        amt = _inventory_db[item]
        c.execute("INSERT INTO inventory (mfg, lqr, amt) VALUES (?, ?, ?)", (mfg, lqr, amt))

    for item in _recipes:
        # add the pickle pointer to dereference on load
        s = cPickle.dumps(item)
        c.execute("INSERT INTO recipes (recipe) VALUES (?)", [sqlite3.Binary(s)])

    conn.commit()
    conn.close()



def load_db_tables(db_name):

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT * FROM bottle_types" ).fetchall()
    bt = c.fetchall()
    for mfg,lqr,typ in bt:	
	add_bottle_type(mfg,lqr,typ)


    c.execute("SELECT * FROM inventory")
    inv = c.fetchall()
    for mfg,lqr,amt in inv:
	# TODO: make cases for units based on amt
	add_to_inventory(mfg,lqr, str(amt) + ' ml')

    rs = c.execute("SELECT * FROM recipes")
    for item in rs:
	pass
	# dereference on load
	#add_recipe( cPickle.loads( str(item[0]) ) )

    print "RECIPES: "
    print _recipes

    conn.close()


def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))


def add_bottle_type_table(mfg, liquor, typ):
    conn = sqlite3.connect('tables.db')
    c = conn.cursor()

    c.execute("INSERT INTO bottle_types (mfg,lqr,typ) VALUES (?,?,?)",(mfg,liquor,typ))

    conn.commit()
    conn.close()

    print_contents('tables.db')


def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False


def _check_bottle_type_exists_table(mfg, liquor):
    conn = sqlite3.connect('tables.db')
    c = conn.cursor()

    c.execute("SELECT * FROM bottle_types WHERE mfg=? and lqr=?", (mfg, liquor) )
    if len(c.fetchall()) > 0:
        conn.close()
	return True
    else:
	conn.close()
	return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    # just add it to the inventory database as a tuple, for now.
    key = (mfg, liquor)
    _inventory_db[key] = _inventory_db.get(key, 0.0) + convert_to_ml(amount)

def add_to_inventory_table(mfg, liquor, amount):
    conn = sqlite3.connect('tables.db')
    c = conn.cursor()

    

    conn.commit()
    conn.close()
   
    update_tables('tables.db')
    print_contents('tables.db')

    
def check_inventory(mfg, liquor):
    return ((mfg, liquor) in _inventory_db)

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."

    return _inventory_db.get((mfg, liquor), 0.0)

def convert_to_ml(amount): 
    return unitconversion.convert_to_ml(amount)


def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."

    for m, l in _inventory_db:
        yield m, l

def add_recipe(r):
    _recipes[r.name] = r

def get_recipe(name):
    return _recipes.get(name)

def get_all_recipes():
    return _recipes.values()

def recipes_satisfied():
    available = []
    for rec in _recipes:
        if not rec.need_ingredients():
	    available.append(rec)
    return available

def check_inventory_for_type(generic_type):
    matching_ml = []
    for (m, l, t) in _bottle_types_db:
        if t == generic_type:
            amount = _inventory_db.get((m, l), 0.0)
            matching_ml.append((m, l, amount))

    return matching_ml

