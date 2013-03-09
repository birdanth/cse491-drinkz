#recipe class used to store recipes in db.py
from . import db

class Recipe:
    	
    def __init__(self,name,ing):
	self.name = name
        self.ing = ing
	#self.recipe = (name,[ing]) 

    def __len__(self):
        return len(self.__recipes)

    def add(self,a):
        self.ing.append(a)

    def need_ingredients(r):
	for item in r:
	    yield item

