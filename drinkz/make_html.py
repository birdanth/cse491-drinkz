#! /usr/bin/env python

import recipes
import db
import os


try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

### POPULATE DB 
db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
            
db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                                '4 oz')])
db.add_recipe(r)


r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),
                                         ('vermouth', '1.5 oz')])
db.add_recipe(r)


r = recipes.Recipe('vomit inducing martini', [('orange juice',
                                                   '6 oz'),
                                                  ('vermouth',
                                                   '1.5 oz')])
db.add_recipe(r)


###

def index():
    return  """             
                <a href='liquor_types.html'>Liquor types</a>
                <p>
                <a href='recipes.html'>Recipes</a>
                <p>
                <a href='inventory.html'>Inventory</a>
                """
###

def recipes():
    html = """ Current Recipes \n <ul>"""
    for r in db.get_all_recipes():
            html += '<li>%s<ul>' % r.name
            for name, amount in r.ingredients:
                html+= '<li>%s'% name  
                html+= ' - %s'% amount
            html+= '</ul>'
    html += """</ul>"""
    return html

    
###


###

fp = open('html/liquor_types.html', 'w')
print >>fp, '<ul>'
for m, l, g in db._bottle_types_db:
    print >>fp, '<li>', m, '--', l, '--', g
print >>fp, '</ul>'


fp = open('html/liquor_inventory.html', 'w')
print >>fp, '<ul>'
for m, l in db.get_liquor_inventory():
    amount = db.get_liquor_amount(m, l)
    print >>fp, '<li>', m, '--', l, '--', amount
print >>fp, '</ul>'
