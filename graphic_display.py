import matplotlib.pyplot as plt
import numpy as np 
import math

import celestial_body as c_b
import constants as cst
import parameters as prm
import numerical_integration as n_i
import utility_functions as u_f
import maneuver
import matplotlib.animation as animation

class MainDisplay : 

	def __init__ (self, satellite_list, celestial_bodies_list) : 


		self.app_name = "Spatial View"
		if(self.app_name == prm.parameters["applications"]["leader application"]) : self.leader = True
		else : self.leader = False


		plt.style.use('dark_background')

		self.figure, self.ax =  plt.subplots()

		cur_axes = plt.gca()
		cur_axes.axes.get_xaxis().set_visible(False)
		cur_axes.axes.get_yaxis().set_visible(False)

		self.ax.set_xlim([-50e11, 50e11])
		self.ax.set_ylim([-50e11, 50e11])

		self.display_mode = prm.parameters["spatial view"]["display mode"]
		self.following_mode = prm.parameters["spatial view"]["following mode"]
		
		try :
			self.body_to_follow = [body for body in (satellite_list+celestial_bodies_list) if body.name == prm.parameters["spatial view"]["body to follow"]][0]
		except : 
			self.body_to_follow = None
		
		self.satellite_list = np.array([])
		self.celestial_bodies_list = np.array([])

		self.satellite_points = np.array([])
		self.celestial_bodies_points = np.array([])

		self.celestial_bodies_traj = np.array([])

		if(self.display_mode == "trajectory prediction") :
			self.satellite_traj = np.array([])

		else : 
			self.satellite_path = np.array([])
			self.x_matrix = np.zeros((len(satellite_list), 1))
			self.y_matrix = np.zeros((len(satellite_list), 1))


		for satellite in satellite_list : 
			self.satellite_list = np.append(self.satellite_list, satellite)

			point, = self.ax.plot([], [], ls="none", marker="o", color=satellite.color)
			self.satellite_points = np.append(self.satellite_points, point)
			
			if(self.display_mode == "trajectory prediction") :
				traj, = self.ax.plot([],[], color=satellite.color)
				self.satellite_traj = np.append(self.satellite_traj, traj)

			else :
				path, = self.ax.plot([],[], ls="-", color=satellite.color)
				self.satellite_path = np.append(self.satellite_path, path)

		for body in celestial_bodies_list :
			self.celestial_bodies_list = np.append(self.celestial_bodies_list, body)

			point, = self.ax.plot([], [], ls="none", marker="o", color=body.color)
			self.celestial_bodies_points = np.append(self.celestial_bodies_points, point)
			traj, = self.ax.plot([],[],ls="-" ,color=body.color)
			self.celestial_bodies_traj = np.append(self.celestial_bodies_traj, traj)

	def update (self, i) :

		if(self.leader == True) :
			u_f.Computation(self.satellite_list, self.celestial_bodies_list)

		if (self.following_mode) : 
			self.ax.set_xlim([self.body_to_follow.r_abs[0]-prm.parameters["spatial view"]["window radius"], self.body_to_follow.r_abs[0]+prm.parameters["spatial view"]["window radius"]])
			self.ax.set_ylim([self.body_to_follow.r_abs[1]-prm.parameters["spatial view"]["window radius"], self.body_to_follow.r_abs[1]+prm.parameters["spatial view"]["window radius"]])
		if(self.display_mode != "trajectory prediction" and i>0) : 
			self.x_matrix = np.append(self.x_matrix, np.zeros((len(self.satellite_list), 1)), axis=1)
			self.y_matrix = np.append(self.y_matrix, np.zeros((len(self.satellite_list), 1)), axis=1)

		for j in range (len(self.satellite_points)) : 
			self.satellite_points[j].set_data(self.satellite_list[j].r_abs[0], self.satellite_list[j].r_abs[1])

			if(self.display_mode == "trajectory prediction") :
				self.satellite_traj[j].set_data(self.satellite_list[j].orbit.traj[0]+self.satellite_list[j].corps_ref.r_abs[0], 
												self.satellite_list[j].orbit.traj[1]+self.satellite_list[j].corps_ref.r_abs[1])
			else :
				self.x_matrix[j][i] = self.satellite_list[j].r_abs[0]
				self.y_matrix[j][i] = self.satellite_list[j].r_abs[1]
				self.satellite_path[j].set_data(self.x_matrix[j][1:i+1], self.y_matrix[j][1:i+1])

		for j in range (len(self.celestial_bodies_points)) :

			 self.celestial_bodies_points[j].set_data(self.celestial_bodies_list[j].r_abs[0], self.celestial_bodies_list[j].r_abs[1])

			 if((self.celestial_bodies_list[j].moving_body == True) or (i == 0 and self.celestial_bodies_list[j].corps_ref is not None)) : 
			 	self.celestial_bodies_traj[j].set_data(self.celestial_bodies_list[j].orbit.traj[0]+self.celestial_bodies_list[j].corps_ref.r_abs[0], 
													   self.celestial_bodies_list[j].orbit.traj[1]+self.celestial_bodies_list[j].corps_ref.r_abs[1])

		if(self.display_mode == "trajectory prediction") :
			return np.concatenate([self.satellite_points, self.celestial_bodies_points, self.satellite_traj, self.celestial_bodies_traj])
		else :
			return np.concatenate([self.satellite_points, self.celestial_bodies_points, self.satellite_path, self.celestial_bodies_traj])


class GroundTrackDisplay : # /!\ ALWAYS PUT THE PARAMETER "BLIT" ON "TRUE" WHEN DISPLAYING A GROUND TRACK /!\

	def __init__ (self, satellite_list, celestial_bodies_list) :


		self.app_name = "Ground Track"
		if(self.app_name == prm.parameters["applications"]["leader application"]) : 
			self.leader = True
		else : self.leader = False


		plt.style.use('dark_background')
		img = plt.imread("mappemonde.jpg")

		self.figure, self.ax = plt.subplots()
		self.ax.imshow(img, extent=[0, 2048, 0, 1024])

		self.satellite_list = satellite_list
		self.celestial_bodies_list = celestial_bodies_list

		self.ground_tracks = np.array([])
		self.x_matrix = np.zeros((len(satellite_list), 1))
		self.y_matrix = np.zeros((len(satellite_list), 1))

		for sat in satellite_list : 
			ground_track, = self.ax.plot([],[], linestyle = 'none', marker = 'o', c = sat.color, markersize = 1)
			self.ground_tracks = np.append(self.ground_tracks, ground_track)

	def update (self, i) : 

		if(self.leader == True) :
			u_f.Computation(self.satellite_list, self.celestial_bodies_list)

		self.x_matrix = np.append(self.x_matrix, np.zeros((len(self.satellite_list), 1)), axis=1)
		self.y_matrix = np.append(self.y_matrix, np.zeros((len(self.satellite_list), 1)), axis=1)

		for j in range (len(self.satellite_list)) :

			self.x_matrix[j][i] = self.satellite_list[j].longitude*180/math.pi*5.688+1024
			self.y_matrix[j][i] = self.satellite_list[j].latitude*180/math.pi*5.688+512
			self.ground_tracks[j].set_data(self.x_matrix[j][max(0, i-250):i+1], self.y_matrix[j][max(0, i-250):i+1])

		return self.ground_tracks


class GraphDisplay : 

	def __init__ (self, satellite_list, celestial_bodies_list) : 


		self.app_name = "Parameters Plot"
		if(self.app_name == prm.parameters["applications"]["leader application"]) : 
			self.leader = True
		else : self.leader = False

		self.func_dictionnary = {
								"Distance to referent body" : self.getDistanceToReferentBody,
								"Distance to central body" : self.getDistanceToCentralBody,
								"Distance to other body" : self.getDistanceToOtherBody,
								"Speed relative to referent body" : self.getSpeedRelativeToReferentBody,
								"Speed relative to central body" : self.getSpeedRelativeToCentralBody,
								"True anomaly" : self.getTrueAnomaly,
								"Longitude" : self.getLongitude,
								"Latitude" : self.getLatitude,
								"Semi major-axis" : self.getSemiMajorAxis,
								"Eccentricity" : self.getEccentricity,
								"Longitude of ascending node" : self.getLongitudeOfAscendingNode,
								"Longitude of perigee" : self.getLongitudeOfPerigee
								}
		

		plt.style.use('dark_background')
		self.figure, self.ax =  plt.subplots()

		self.ax.set_xlim([0, 1e3])
		self.ax.set_ylim([0, 360])

		self.max = -1e10
		self.min =  1e10

		self.satellite_list = satellite_list
		self.celestial_bodies_list = celestial_bodies_list

		requested_func = prm.parameters["parameters plot"]["parameter to plot"]
		args = prm.parameters["parameters plot"]["satellites displayed"]

		self.body_list = [body for body in np.concatenate((self.satellite_list, self.celestial_bodies_list)) if (body.name in args)]
		self.func_to_call = self.func_dictionnary.get(requested_func)

		self.time = np.array([])
		self.recorded_data = np.zeros((len(self.body_list), 1))

		self.curves = np.array([])
		for body in self.body_list : 
			curve, = self.ax.plot([],[], ls="-", color=body.color)
			self.curves = np.append(self.curves, curve)


	def update (self, i) : 

		self.ax.set_xlim([prm.parameters["time"]["elapsed time"]-prm.parameters["parameters plot"]["historic length"], prm.parameters["time"]["elapsed time"]+10])
		self.ax.set_ylim([self.min-0.1*self.min, self.max+0.1*self.max])

		if(self.leader == True) :
			u_f.Computation(self.satellite_list, self.celestial_bodies_list)

		new_data = self.func_to_call(self.body_list)
		self.recorded_data = np.append(self.recorded_data, np.zeros((len(self.body_list), 1)), axis=1)

		for data in new_data : 
			if(data < self.min) : self.min = data
			elif(data > self.max) : self.max = data

		self.time = np.append(self.time, prm.parameters["time"]["elapsed time"])

		for j in range(len(self.curves)) :
			self.recorded_data[j][i] = new_data[j]
			self.curves[j].set_data(self.time[:i], self.recorded_data[j][:i])

		return self.curves


	def getDistanceToReferentBody (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.r_cr_norm)
		return list_

	def getDistanceToCentralBody (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.r_abs_norm)
		return list_

	def getDistanceToOtherBody (*bodies) : 
		return [np.linalg.norm(bodies[0][0].r_abs-bodies[0][1].r_abs)]

	def getSpeedRelativeToReferentBody (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.v_cr_norm)
		return list_

	def getSpeedRelativeToCentralBody (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.v_abs_norm)
		return list_

	def getTrueAnomaly (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.true_anomaly*180/math.pi)
		return list_

	def getLongitude (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.longitude*180/math.pi)
		return list_

	def getLatitude (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.latitude*180/math.pi)
		return list_

	def getSemiMajorAxis (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.a)
		return list_

	def getEccentricity (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.e)
		return list_

	def getLongitudeOfAscendingNode (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.Lnode*180/math.pi)
		return list_

	def getLongitudeOfPerigee (*bodies) : 
		list_ = list()
		for body in bodies[0] : 
			list_.append(body.Lperi*180/math.pi)
		return list_








