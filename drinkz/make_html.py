#! /usr/bin/env python

import recipes
import db
import os


try:
    os.mkdir('html')
except OSError:
    # already exists
    pass


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

def index():
    return  """
            <html style="background-color:gray" >
                <head style="font-family:verdana;">
                    <title>Index</title>
                    <style type ="text/css"> h1{color:red;text-align:center;} </style>
                    <script type="text/javascript">
                        function test_alert()
                        {
                            alert("Testing Alert System");
                        }
                    </script>
                </head>
                <body style="text-align:left" >
                    <h1>cse491-drinkz </h1>
                    <p style="text-align:center">
                    <input type="button" onclick="test_alert()" value="Alert System"  />
                    </p>
                    <a href='liquor_types.html'>Liquor types</a>
                    <p>
                    <a href='recipes.html'>Recipes</a>
                    <p>
                    <a href='inventory.html'>Inventory</a>
                    <p>
                    <a href='conversion.html'>Convert to ML </a>
                </body>
            </html>
            """
###
def liquor_types():
    html = """<title>Liquor Types</title>
                  <h1 style="color:red" >Liquor Types </h1> 


              <ul>
           """
    for m, l, g in db._bottle_types_db:
        html += '<li>%s' % m
        html += ' - %s' % l
        html += ' - %s</li>' % g
    html += """</ul>"""
    html += "<a href='index.html'> HOME </a>"
    return html

###


def recipes():
    html = """<title>Recipes</title>
                  <h1 style="color:red" >Recipes </h1> 


              <ul>
           """
    for r in db.get_all_recipes():
            html += '<li>%s<ul>' % r.name
            for name, amount in r.ingredients:
                html+= '<li>%s'% name  
                html+= ' - %s'% amount
            html+= '</ul>'
    html += """</ul>"""
    html += "<a href='index.html'> HOME </a>"
    return html

    


###

def inventory():
    html = """<title>Inventory</title>
                  <h1 style="color:red" >Inventory </h1> 


              <ul>
           """
    for m, l in db.get_liquor_inventory():
        amount = db.get_liquor_amount(m, l)
        html += '<li>%s' % m
        html += ' - %s' % l
        html += ' - %s</li>' % amount
    html += """</ul>"""
    html += "<a href='index.html'> HOME </a>"
    return html

###

def conversion_form():
    return """ <title>Unit Converter</title>
                <h1 style="color:red" >Unit Converter</h1>
                    <form action='converter_recv'>
                        Amount? <input type='text' name='inputValue' size'20'>
                        <input type='submit'>
                    </form>
            """


