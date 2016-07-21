###Code for checking if passed value divides into another, and output is a whole number

def isWhole(x):
	e = x/20          #Value divided into 20
	if (e%1 == 0):
		return x      #Return input value if whole
	else:
		return 0      #Return 0 if value is decimal