#recipe class used to store recipes in db.py
from . import db

class Recipe:
    	
    def __init__(self,name,ing):
	self.name = name
        self.ing = ing
	#self.recipe = (name,[ing]) 

    def need_ingredients(self):
	needed = []
	for (generic_type,amount) in self.ing:
	    matching = db.check_inventory_for_type(generic_type)

	    max_m = ''
	    max_l = ''
	    max_amount = 0.0

	    for (m,l,t) in matching:
	        if t > max_amount:
	            max_amount = t 

	    amount_needed db.convert_to_ml(amount)

	    if max_amount < amount_needed:
	        needed.append((generic_type, amount_needed - max_amount))
	
	    return needed 
