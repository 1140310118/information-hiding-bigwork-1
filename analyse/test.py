from scipy.optimize import fsolve
from math import cos,sin

def f(x):
	x0=float(x[0])
	x1=float(x[1])
	x2=float(x[2])
	return [x0,x1-1,x2-1]

result=fsolve(f,[1,1,1])
print (result)
print (f(result))