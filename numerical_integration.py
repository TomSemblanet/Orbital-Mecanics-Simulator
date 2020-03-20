import numpy as np 
import matplotlib.pyplot as plt 
import math

import satellite as sat
import celestial_body as c_b
import parameters as prm

def burlirsch_stoer_method (satellite, time, A, N, Y, m, adapted_thrust=False) :

	for j in range (prm.jmax+1) :

		A[j][0] = satellite.pas_pointmilieu_modifie(prm.H, time, Y, m[j], adapted_thrust)

		for i in range (1,j+1) :
			correction = (A[j][i-1]-A[j-1][i-1])/((m[j]*1.0/m[j-i])**2-1)
			A[j][i] = A[j][i-1] + correction
		
		e = 0.0

		for k in range (N) : 
			e+=(abs(A[j][j][k]-A[j][j-1][k])/(prm.atol+prm.rtol*abs(A[j][j][k])))**2
		e = np.sqrt(e/N)
		if(e<1):
			break

	return np.array(A[j][j])