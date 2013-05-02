import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp
from . import db, load_bulk_data, recipes


def test_add_bottle_type_to_database():
    print 'Bottle type not added to data table!'

    db._reset_db()

    db.add_bottle_type_table('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists_table('Johnnie Walker', 'Black Label')


def test_add_to_inventory_database():
    print 'Bottle type not added to data table!'

    db._reset_db()

    db.add_bottle_type_table('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists_table('Johnnie Walker', 'Black Label')

def test_save_to_db():
    print 'trying to save to sql db'

    db._reset_tables('tables.db')
    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                               '4 oz')])

    db.add_recipe(r)
    db.save_db_tables('tables.db')
    print db.print_contents('tables.db')

    assert True

def test_load_from_db():

    print 'LOADING FROM DATABASE'

    db.load_db_tables('tables.db')

    assert True


def test_pairings():
  
    print 'PAIRINGS!!!!'
    
    print db.get_pairings()

    assert False
