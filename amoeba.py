import math
import numpy
import random
import cake

class amoeba:
	def __init__(self, master, center_coords=numpy.zeros(2)):
		self.master = master

		self.center_coords = center_coords
		self.circle_res = 8
		self.circle_radius = 100.
		
		self.node_mass = 1.0
		self.treading = 3
		self.treadk = 1000.
		
		self.musclek = 1000.
		self.muscle_period = .4
		self.muscle_amp = 100.
	
	def assemble(self):
		# setup
		self.circle_res *= 2
		
		# unit circle generation
		self.circle = []
		for i in range(0,self.circle_res):
			posx = numpy.cos(i*2.0*math.pi/self.circle_res)
			posy = numpy.sin(i*2.0*math.pi/self.circle_res)
			# mass transform
			posx *= self.circle_radius
			posy *= self.circle_radius
			posx += self.center_coords[0]
			posy += self.center_coords[1]
			# node creation
			newnode = self.master.make_node(self.node_mass, numpy.array([posx, posy])) #FLAG!!!
			self.circle.append(newnode)
		
		# tread generator
		self.tread = []
		for r in range(1,self.treading+1):
			for i in range(0,self.circle_res):
				length = numpy.linalg.norm(self.circle[i].pos - self.circle[i-r].pos)
				self.tread.append( self.master.make_spring(self.circle[i], self.circle[i-r], float(length), self.treadk) )
		
		# muscle generator
		self.muscle_count = self.circle_res/2
		self.muscles = []
		self.muscle_length = self.circle_radius*2
		#muscle_length = numpy.linalg.norm(circle[i].pos - circle[i-4].pos) # should be at least close
		for i in range(0,self.muscle_count):
			self.muscles.append( self.master.make_spring(self.circle[i], self.circle[i-self.muscle_count], self.circle_radius*2, self.musclek) )
	
	def update(self, simtime):
		for m in range(0,self.muscle_count):
			self.muscles[m].targl = self.muscle_amp * numpy.sin( (simtime/self.muscle_period) + (m*2*math.pi/self.muscle_count) )
			self.muscles[m].targl += self.muscle_length