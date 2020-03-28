import numpy as np 
import matplotlib.pyplot as plt 
import math

import satellite as sat
import celestial_body as c_b
import parameters as prm

# jmax = 10
# N = 6  
# A = np.zeros((jmax+1, jmax+1, N))
# m = 2*(np.arange(jmax+1)+1)
# atol = 1e-12
# rtol= 1e-5

# def pas_pointmilieu_modifie (satellite, Yn, m, adapted_thrust=False) :

# 		H = prm.parameters["time"]["time step"]
# 		t = prm.parameters["time"]["elapsed time"]

# 		h = H/m
# 		u = Yn
# 		v = u+h*satellite.calculateAcceleration(u,t, adapted_thrust)
# 		for k in range(1,m):
# 			w = u+2*h*satellite.calculateAcceleration(v,t+k*h, adapted_thrust)
# 			u = v
# 			v = w

# 		return 0.5*(v+u+h*satellite.calculateAcceleration(v,t+H, adapted_thrust))


# def burlirsch_stoer_method (satellite, Y, adapted_thrust=False) :

# 	for j in range (jmax+1) :

# 		A[j][0] = pas_pointmilieu_modifie(satellite, Y, m[j], adapted_thrust)

# 		for i in range (1,j+1) :
# 			correction = (A[j][i-1]-A[j-1][i-1])/((m[j]*1.0/m[j-i])**2-1)
# 			A[j][i] = A[j][i-1] + correction
		
# 		e = 0.0

# 		for k in range (N) : 
# 			e+=(abs(A[j][j][k]-A[j][j-1][k])/(atol+rtol*abs(A[j][j][k])))**2
# 		e = np.sqrt(e/N)
# 		if(e<1):
# 			break

# 	return np.array(A[j][j])


def RK4 (state_vector) :

	r = state_vector[:3]
	v = state_vector[3:]
	dt = prm.parameters['time']['time step']

	k1_r = v
	k1_v = sat.calculateAcceleration(r)
	
	k2_r = v + k1_v*dt/2
	k2_v = sat.calculateAcceleration(r + k1_r*dt/2)

	k3_r = v + k2_v*dt/2
	k3_v = sat.calculateAcceleration(r + k2_r*dt/2)

	k4_r = v + k3_v*dt
	k4_v = sat.calculateAcceleration(r + k3_r*dt)

	state_vector[:3] = r + dt/6*(k1_r + 2*k2_r + 2*k3_r + k4_r)
	state_vector[3:] = v + dt/6*(k1_v + 2*k2_v + 2*k3_v + k4_v)

	return state_vector







