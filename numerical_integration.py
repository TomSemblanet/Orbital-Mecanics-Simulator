import numpy as np 
import matplotlib.pyplot as plt 
import math

import satellite as sat
import celestial_body as c_b
import parameters as prm

jmax = 10
N = 6  
A = np.zeros((jmax+1, jmax+1, N))
m = 2*(np.arange(jmax+1)+1)
atol = 1e-12
rtol= 1e-5

def burlirsch_stoer_method (satellite, time, A, N, Y, m, adapted_thrust=False) :

	for j in range (jmax+1) :

		A[j][0] = satellite.pas_pointmilieu_modifie(prm.parameters["time"]["time step"], time, Y, m[j], adapted_thrust)

		for i in range (1,j+1) :
			correction = (A[j][i-1]-A[j-1][i-1])/((m[j]*1.0/m[j-i])**2-1)
			A[j][i] = A[j][i-1] + correction
		
		e = 0.0

		for k in range (N) : 
			e+=(abs(A[j][j][k]-A[j][j-1][k])/(atol+rtol*abs(A[j][j][k])))**2
		e = np.sqrt(e/N)
		if(e<1):
			break

	return np.array(A[j][j])