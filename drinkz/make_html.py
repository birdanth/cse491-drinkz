#! /usr/bin/env python

import recipes
import db
import os
from jinja2 import Environment, PackageLoader

### make a directory to store the generated html files
try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

### Initialize the html templates - http://jinja.pocoo.org/docs/api/
env = Environment( loader = PackageLoader('drinkz', 'html-templates') )
print env
    
### POPULATE DB (from file or inline)

try:
    db.load_db('initDatabase')
except:
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

def baseTemplate():
    base =  env.get_template('base.html')
    return base.render()
    

def index():
    index = env.get_template('index.html')
    #print index - use encode('ascii','ignore') to return string value
    return index.render().encode('ascii', 'ignore')

def liquor_types():
    html = ""    
    for m, l, g in db._bottle_types_db:
        html += '<li>%s' % m
        html += ' - %s' % l
        html += ' - %s</li>' % g
    html += """</ul>"""

    liquorTypes =  env.get_template('liquor_types.html')
    return liquorTypes.render(liquor_types=html).encode('ascii', 'ignore')

def add_to_liquor_types():
    addToLiquorTypes =  env.get_template('add_to_liquor_types.html')
    return addToLiquorTypes.render().encode('ascii', 'ignore')

def recipes():
    html = ""
    for r in db.get_all_recipes():
            html += '<li>%s<ul>' % r.name
            for name, amount in r.ingredients:
                html+= '<li>%s'% name  
                html+= ' - %s'% amount
            html+= '</ul>'
    html += """</ul>"""
    
    recipes =  env.get_template('recipes.html')
    return recipes.render(recipes=html).encode('ascii', 'ignore')

    
def add_to_recipes():
    addToRecipes =  env.get_template('add_to_recipes.html')
    return addToRecipes.render().encode('ascii', 'ignore')


def inventory():
    html = ""
    for m, l in db.get_liquor_inventory():
        amount = db.get_liquor_amount(m, l)
        html += '<li>%s' % m
        html += ' - %s' % l
        html += ' - %s</li>' % amount
    html += """</ul>"""

    inv =  env.get_template('inventory.html')
    return inv.render(inventory=html).encode('ascii', 'ignore')


def add_to_inventory():
    addToInventory =  env.get_template('add_to_inventory.html')
    return addToInventory.render().encode('ascii', 'ignore')



def conversion_form():
    conversion =  env.get_template('conversion.html')
    return conversion.render().encode('ascii', 'ignore')



