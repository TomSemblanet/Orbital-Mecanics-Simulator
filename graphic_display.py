import matplotlib.pyplot as plt
import numpy as np 
import math

import celestial_body as c_b
import constants as cst
import numerical_integration as n_i
import utility_functions as u_f
import maneuver
import matplotlib.animation as animation

class MainDisplay : 

	def __init__ (self, satellite_list, celestial_bodies_list, display_mode="trajectory prediction", following_mode=False, parameters_on=False, simulation_speed="slow") : 

		plt.style.use('dark_background')
		# plt.style.use('seaborn-dark')

		self.figure, self.ax =  plt.subplots()

		cur_axes = plt.gca()
		cur_axes.axes.get_xaxis().set_visible(False)
		cur_axes.axes.get_yaxis().set_visible(False)

		self.ax.set_xlim([-4e8, 4e8])
		self.ax.set_ylim([-4e8, 4e8])

		if(simulation_speed=="slow") : self.calculation_repeat = 1
		elif(simulation_speed=="medium") : self.calculation_repeat = 2 
		elif(simulation_speed=="high") : self.calculation_repeat = 3
		elif(simulation_speed=="very high") : self.calculation_repeat = 4

		self.display_mode = display_mode
		self.following_mode = following_mode
		self.parameters_on = parameters_on
		
		self.satellite_list = np.array([])
		self.celestial_bodies_list = np.array([])

		self.satellite_points = np.array([])
		self.celestial_bodies_points = np.array([])

		self.celestial_bodies_traj = np.array([])

		self.value = celestial_bodies_list[0].mu

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
			traj, = self.ax.plot([],[], color=body.color)
			self.celestial_bodies_traj = np.append(self.celestial_bodies_traj, traj)

	def update (self, i) :

		if(self.parameters_on) : 	
			u_f.display_parameters(self.satellite_list)

		for b in range (self.calculation_repeat) :  # repetition allow the programm to reduce the computational time by reducing the number of plot
		
			u_f.update_celestial_bodies_position(self.celestial_bodies_list)
			u_f.satellites_accelerations(self.satellite_list)
			u_f.update_ref_body(self.satellite_list, self.celestial_bodies_list)
			u_f.update_date()

		if (self.following_mode) : 
			self.ax.set_xlim([self.satellite_list[0].r_abs[0]-50000e3, self.satellite_list[0].r_abs[0]+50000e3])
			self.ax.set_ylim([self.satellite_list[0].r_abs[1]-50000e3, self.satellite_list[0].r_abs[1]+50000e3])
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

			 if(i == 0 and self.celestial_bodies_list[j].corps_ref is not None) : 
			 	self.celestial_bodies_traj[j].set_data(self.celestial_bodies_list[j].orbit.traj[0]+self.celestial_bodies_list[j].corps_ref.r_abs[0], 
													   self.celestial_bodies_list[j].orbit.traj[1]+self.celestial_bodies_list[j].corps_ref.r_abs[1])

		if(self.display_mode == "trajectory prediction") :
			return np.concatenate([self.satellite_points, self.celestial_bodies_points, self.satellite_traj, self.celestial_bodies_traj])
		else :
			return np.concatenate([self.satellite_points, self.celestial_bodies_points, self.satellite_path, self.celestial_bodies_traj])


class GroundTrackDisplay : # /!\ ALWAYS PUT THE PARAMETER "BLIT" ON "TRUE" WHEN DISPLAYING A GROUND TRACK /!\

	def __init__ (self, satellite_list) :

		plt.style.use('seaborn-pastel')
		img = plt.imread("mappemonde.jpg")
		self.figure, self.ax = plt.subplots()
		self.ax.imshow(img, extent=[0, 2048, 0, 1024])

		self.satellite_list = satellite_list

		self.ground_tracks = np.array([])
		self.x_matrix = np.zeros((len(satellite_list), 1))
		self.y_matrix = np.zeros((len(satellite_list), 1))

		for sat in satellite_list : 
			ground_track, = self.ax.plot([],[], linestyle = 'none', marker = 'o', c = sat.color, markersize = 1)
			self.ground_tracks = np.append(self.ground_tracks, ground_track)

	def update (self, i) : 

		self.x_matrix = np.append(self.x_matrix, np.zeros((len(self.satellite_list), 1)), axis=1)
		self.y_matrix = np.append(self.y_matrix, np.zeros((len(self.satellite_list), 1)), axis=1)

		for j in range (len(self.satellite_list)) :

			self.x_matrix[j][i] = self.satellite_list[j].longitude*180/math.pi*5.688+1024
			self.y_matrix[j][i] = self.satellite_list[j].latitude*180/math.pi*5.688+512
			self.ground_tracks[j].set_data(self.x_matrix[j][max(0, i-200):i+1], self.y_matrix[j][max(0, i-200):i+1])

		return self.ground_tracks


class GraphDisplay : 

	def __init__ (self, data_name, body1, body2=None) : 
		
		plt.style.use('dark_background')
		self.figure, self.ax =  plt.subplots()
		self.ax.set_ylim([0, 200e3])

		self.xlim = 10e3

		self.curve, = self.ax.plot([],[], ls='-', color='c')

		self.time = np.array([])
		self.data = np.array([])

		self.body1 = body1
		self.body2 = body2

		self.data_name = data_name

	def update (self, i) : 

		self.ax.set_xlim([-self.xlim+cst.time, self.xlim+cst.time])

		if(self.data_name == "distance (reference body)") : 
			self.data = np.append(self.data, self.body1.r_cr_std/1000)
		elif(self.data_name == "distance (main body)") : 
			self.data = np.append(self.data, self.body1.r_abs_std/1000)
		elif(self.data_name == "velocity (reference body)") : 
			self.data = np.append(self.data, self.body1.v_cr_std/1000)
		elif(self.data_name == "velocity (main body)") : 
			self.data = np.append(self.data, self.body1.v_abs_std/1000)
		elif(self.data_name == "true anomaly") : 
			self.data = np.append(self.data, self.body1.true_anomaly*180/math.pi)
		elif(self.data_name == "distance (second body)") : 
			self.data = np.append(self.data, np.linalg.norm(self.body1.r_cr - self.body2.r_cr)/1000)
		elif(self.data_name == "angle") : 
			self.data = np.append(self.data, math.acos(np.dot(self.body1.v_abs, [1, 0, 0])/self.body1.v_abs_std)*180/math.pi)

		self.time = np.append(self.time, cst.time)

		self.curve.set_data(self.time[:i], self.data[:i])

		return self.curve








