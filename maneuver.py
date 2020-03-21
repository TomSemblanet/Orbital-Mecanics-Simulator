import matplotlib.pyplot as plt
import numpy as np 
import math

import celestial_body as c_b
import parameters as prm
import numerical_integration as n_i
import utility_functions as u_f

class TriggerDetector : 

	def __init__ (self, satellite, type, trigger_value) : 

		self.dict = {"true anomaly": getattr(TriggerDetector, 'TargetedTrueAnomalySupervisor'), 
					 "date" : getattr(TriggerDetector, 'TargetedTimeSupervisor')} 

		self.satellite = satellite
		self.trigger_value = trigger_value
		self.trigger_time = self.dict.get(type)(self)


	def TargetedTrueAnomalySupervisor (self) : 
		t = u_f.PassageTimePredictor(self.satellite, self.trigger_value)
		if(t<1e-5) : t = self.satellite.orbit.T
		return t

	def TargetedTimeSupervisor (self) : 
		return u_f.DateToSeconds(prm.starting_date, self.trigger_value)

	def TriggerTimeSupervisor (self) : 
		if(abs(prm.elapsed_time - self.trigger_time) <= prm.H) :
			if(abs(prm.elapsed_time - self.trigger_time) != 0) :
				prm.H =  abs(prm.elapsed_time - self.trigger_time)
			else : 
				return True

		return False


class OrbitModificationManeuver : 

	def __init__ (self, satellite, name, modification_value, angle=None) :

		self.dict = {"apogee modification": getattr(OrbitModificationManeuver, 'ApogeeModificationLoader'), 
					 "perigee modification": getattr(OrbitModificationManeuver, 'PerigeeModificationLoader'),
					 "inclinaison modification" : getattr(OrbitModificationManeuver, 'InclinaisonModificationLoader')}

		self.satellite = satellite
		self.modification_value = modification_value

		self.dV, self.direction = self.dict.get(name)(self)


	def ApogeeModificationLoader (self) : 
		
		if(self.modification_value >= 0) : 
			dV = math.sqrt( 2*self.satellite.corps_ref.mu*(1/(self.satellite.orbit.a*(1-self.satellite.orbit.e)) - 1/(2*self.satellite.orbit.a)) + self.satellite.corps_ref.mu*(1/self.satellite.orbit.a - 1/(self.satellite.orbit.a+0.5*self.modification_value)) ) - math.sqrt( 2*self.satellite.corps_ref.mu*(1/(self.satellite.orbit.a*(1-self.satellite.orbit.e)) - 1/(2*self.satellite.orbit.a)) )		
		else : 
			dV = -(math.sqrt( 2*self.satellite.corps_ref.mu*( 1/(self.satellite.orbit.a*(1-self.satellite.orbit.e)) - 1/(2*self.satellite.orbit.a))) - math.sqrt( 2*self.satellite.corps_ref.mu*( 1/(self.satellite.orbit.a*(1-self.satellite.orbit.e)) - 1/(2*self.satellite.orbit.a+self.modification_value))))

		direction = np.array([0., 0., 0.])

		return (dV, direction)

	def PerigeeModificationLoader (self) : 
		
		if(self.modification_value >= 0) : 
			dV = math.sqrt( 2*self.satellite.corps_ref.mu*(1/(self.satellite.orbit.a*(1+self.satellite.orbit.e)) - 1/(2*self.satellite.orbit.a)) + self.satellite.corps_ref.mu*(1/self.satellite.orbit.a - 1/(self.satellite.orbit.a+0.5*self.modification_value)) ) - math.sqrt( 2*self.satellite.corps_ref.mu*(1/(self.satellite.orbit.a*(1+self.satellite.orbit.e)) - 1/(2*self.satellite.orbit.a)) )
		else : 
			self.modification_value = -self.modification_value
			dV = -(math.sqrt( 2*self.satellite.corps_ref.mu*( 1/(self.satellite.orbit.a*(1+self.satellite.orbit.e)) - 1/(2*self.satellite.orbit.a) ) ) - math.sqrt( 2*self.satellite.corps_ref.mu*( 1/(self.satellite.orbit.a*(1+self.satellite.orbit.e)) - 1/(2*self.satellite.orbit.a+self.modification_value))))

		direction = np.array([0., 0., 0.])

		return (dV, direction)

	def InclinaisonModificationLoader (self) : 

		self.modification_value = self.modification_value*(math.pi/180)
		dV = 2*self.satellite.v_cr_std*math.sin(abs(self.modification_value)/2)
		direction = math.cos(abs(self.modification_value)/2)*(self.satellite.h/self.satellite.h_std) - math.sin(abs(self.modification_value)/2)*(self.satellite.v_cr/self.satellite.v_cr_std)
		if(self.modification_value < 0) :
			direction[2] = -direction[2]

		return (dV, direction)


class FreeAcceleration : 

	def __init__ (self, satellite, dV, direction) : 
		
		self.satellite = satellite
		self.dV = dV
		self.direction = direction

class OrbitalRendezVous : 

	def __init__ (self, satellite, position_to_reach, arrival_time) : 

		self.satellite = satellite
		self.position_to_reach = position_to_reach
		self.arrival_time = arrival_time

		self.dV, self.direction = self.ParameterLoader()

	def ParameterLoader (self) : 

		travel_time = self.arrival_time - prm.elapsed_time

		dV_vector = u_f.LambertProblem(self.satellite.r_abs, self.position_to_reach, travel_time, self.satellite.corps_ref.mu) - self.satellite.v_abs 
		dV = np.linalg.norm(dV_vector)
		direction = dV_vector/dV

		return (dV, direction)


class Maneuver : 

	def __init__ (self, satellite, man_name, value, trigger_type, trigger_value, direction) : 

		self.dict = {"apogee modification": getattr(Maneuver, 'ComputeOrbitalModificationManeuver'), 
					 "perigee modification": getattr(Maneuver, 'ComputeOrbitalModificationManeuver'),
					 "inclinaison modification" : getattr(Maneuver, 'ComputeOrbitalModificationManeuver'),
					 "custom acceleration" : getattr(Maneuver, 'ComputeCustomManeuver'),
					 "orbital rendez-vous" : getattr(Maneuver, 'ComputeOrbitalRendezVous')}

		self.satellite = satellite
		self.trigger_type = trigger_type
		self.trigger_value = trigger_value
		self.man_name = man_name
		self.value = value
		self.direction = direction

		if(trigger_type == "date") : 
			trigger_value = u_f.DateToSeconds(prm.starting_date, trigger_value)

		self.data_loader = self.dict[man_name]

		self.trigger_detector = TriggerDetector(self.satellite, self.trigger_type, self.trigger_value)

		self.maneuver_data = None

	def ComputeOrbitalModificationManeuver (self) : 
		self.maneuver_data = OrbitModificationManeuver(self.satellite, self.man_name, self.value, self.trigger_value)

	def ComputeCustomManeuver (self) : 
		self.maneuver_data = FreeAcceleration(self.satellite, self.value, self.direction)

	def ComputeOrbitalRendezVous (self) :
		self.value["date"] = u_f.DateToSecond(prm.starting_date, self.value["date"])
		self.maneuver_data = OrbitalRendezVous(self.satellite, self.value["position_to_reach"], self.value["date"])



