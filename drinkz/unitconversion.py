#unit conversion

def convert_to_ml(amount):
	num, units = amount.split()
	num = float(num)
	units = units.lower()

	if units == 'ml':
		pass
	elif units == 'liters' or units == 'liter':
		num = 1000.0*num
	elif units == 'oz':
		num = 29.5735*num
	elif units == 'gallons' or units == 'gallon' or units == 'gall':
		num = 3785.41*num
	else:
		print 'unknown unit type, not added to total'

	return num
