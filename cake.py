import numpy
import math
import time

class c_master:
	def __init__(self):
		pass
	
	def make_node(self, i_mass, i_pos, i_vel=numpy.zeros(2)):
		newnode = c_node(self, i_mass, i_pos, i_vel)
		return newnode
	
	def update():
		pass

class c_node:
	def __init__(self, i_master, i_mass, i_pos, i_vel):
		self.master = i_master
		self.pos = i_pos
		self.vel = i_vel
		self.accel = numpy.zeros(2)
		self.mass = i_mass
	
	def push(force):
		self.accel += force/self.mass
	
	def update():
		self.vel += self.accel
		self.pos += self.vel
		self.accel = numpy.zeros(2)