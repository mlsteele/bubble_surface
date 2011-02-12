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
		self.tread_damp = 0.
		
		self.musclek = 1000.
		self.muscle_period = .4
		self.muscle_amp = 100.
		self.muscle_damp = 0.
		
		self.phase = 0.
		self.gofactor = 0.
		
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
				self.tread.append( self.master.make_spring(self.circle[i], self.circle[i-r], float(length), self.treadk, damp=self.tread_damp) )
		
		# muscle generator
		self.muscle_count = self.circle_res/2
		self.muscles = []
		self.muscle_length = self.circle_radius*2
		#muscle_length = numpy.linalg.norm(circle[i].pos - circle[i-4].pos) # should be at least close
		for i in range(0,self.muscle_count):
			self.muscles.append( self.master.make_spring(self.circle[i], self.circle[i-self.muscle_count], self.circle_radius*2, self.musclek, damp=self.muscle_damp) )
	
	def update(self, timestep):
		# how are my feet feeling?
		touch = 0.
		for i in range(0,self.circle_res):
			if self.circle[i].contact:
				touch += 1.
		touchr = touch/self.circle_res
		
#		if (touchr) >= (1./4):
#			self.gofactor += 1.*timestep
#		elif (touch) >= 3:
#			pass
#		else:
#			self.gofactor -= .1*timestep
#			self.gofactor = max(self.gofactor, 0.)
		
		if touch >= 1.:
			self.gofactor += .05*timestep
		else:
			self.gofactor -= .1*timestep
		self.gofactor = min(self.gofactor, 1.)
		self.gofactor = max(self.gofactor, 0.)
		
		# update phase
		self.phase += timestep*self.gofactor
		self.phase = self.phase % self.muscle_period
		
		# run muscles
		for m in range(0,self.muscle_count):
			self.muscles[m].targl = self.muscle_amp * numpy.sin( (self.phase/self.muscle_period*2*math.pi) + (float(m)/self.muscle_count*2*math.pi) )
			self.muscles[m].targl += self.muscle_length
		
		
