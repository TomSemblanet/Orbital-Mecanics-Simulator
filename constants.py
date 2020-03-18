import numpy as np

jmax = 10
N = 6  
A = np.zeros((jmax+1, jmax+1, N))
m = 2*(np.arange(jmax+1)+1)

atol = 1e-12
rtol= 1e-5



T = 1e10
ideal_H = 100
H = ideal_H

r=np.array([0., 0., 0.])
v=np.array([0., 0., 0.])

time = 0

parameters_on = True

simulation_speed_dict = {"slow" : 1, 
						"medium" : 2,
						"high" : 3,
						"very high" : 4}

simulation_speed = "medium"
calculation_repeat = simulation_speed_dict.get(simulation_speed)

applicationsOn = [1]
leaderApplication = min(applicationsOn) # The leader application is the one which will call the calculation at each time step in order to be able
										# to display only the ground track or only the graphical parameters display ...


# mass data [kg]
massSu = 1.9885e30
massMe = 3.3011e23
massVe = 4.8675e24
massTe = 5.97237e24
massMa = 6.4171e23
massJu = 1.8982e27
massSa = 5.6834e26
massUr = 8.6810e25
massNe = 1.02413e26
massLu = 7.34767309e22

# standard gravitational parameter data [m^3/s^2]
muSu = 1.32712440018e20
muMe = 2.2032e13
muVe = 3.24859e14
muTe = 3.986004418e14
muMa = 4.282837e13
muJu = 1.26686534e17
muSa = 3.7931187e16
muUr = 5.793939e15
muNe = 6.836529e15
muLu = 4.9048695e12

# equatorial radius data [m]
radSu = 696342e3
radMe = 2439.7e3
radVe = 6051.8e3
radTe = 6378.137e3
radMa = 3389.5e3
radJu = 69911e3
radSa = 58232e3
radUr = 25362e3
radNe = 24622e3
radLu = 1737.4e3


# rotationnal velocity data [rad/s]

wTe = 7.292115e-5



# ephemerides on 01.01.2000 00:00:00 (heliocentric, rectangular coordinates systeme)

eSu = np.array([0., 0., 0., 0., 0., 0.])
eMe = np.array([-0.1407123544334,   -0.4439062304280,   -0.0233474323330,    0.0211691765227,   -0.0070970127636,   -0.0025227804232])
eVe = np.array([-0.7186298352682,   -0.0225188849760,    0.0411716135761,    0.0005139556873,   -0.0203061283755,   -0.0003071987360])
eTe = np.array([-0.1685374502545,    0.9687810706516,   -0.0000041211671,   -0.0172339077638,   -0.0030078848975,    0.0000000357456])
eMa = np.array([1.3903616215857,   -0.0209984418540,   -0.0346177927372,    0.0007478135638,    0.0151863004077,    0.0002997560322])
eJu = np.array([4.0034566972348,    2.9353584323081,   -0.1018230963104,   -0.0045634805466,    0.0064467525768,    0.0000754565207])
eSa = np.array([6.4085515448418,    6.5680470297778,   -0.3691278222728,   -0.0042911215368,    0.0038915788069,    0.0001028769042])
eUr = np.array([14.4305201906630,  -13.7356550097684,   -0.2381262370293,    0.0026783792149,    0.0026724431971,   -0.0000247775904])
eNe = np.array([16.8107670197170,  -24.9926503203752,    0.1272760867179,    0.0025793709492,    0.0017767692067,   -0.0000959086099])
eMo = np.array([-0.1706605703450,    0.9671638383115,    0.0002402387170,   -0.0169099517768,   -0.0034698287592,   -0.0000009195883])




# general data 

sideral_day  = 86164.1 # duration of a sideral day [s]
solar_day = 86400 # duration of a solar day [s]

J2 = 1.08253e-3 # Coefficient of serial development of terrestrial potential [-]
J3 = -2.54e-6 # Coefficient of serial development of terrestrial potential [-]

equatorial_plan_inclinaison = 0.401425728 # tilt of the earth's equator on the ecliptic one (mean value)

