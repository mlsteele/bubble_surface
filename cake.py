import numpy
import math
import time

class c_master:
	def __init__(self, friction=1., gravity_glob=numpy.zeros(2), ground=False, ground_friction=1):
		self.bucket = []
		self.bucklen = 0
		
		self.friction = friction
		self.gravity_glob = gravity_glob
		self.ground = ground
		self.ground_friction = ground_friction
	
	def make_node(self, i_mass, i_pos, i_vel=numpy.zeros(2)):
		newnode = c_node(self, i_mass, i_pos, i_vel)
		self.register_obj(newnode)
		return newnode
	
	def make_spring(self, i_ma, i_mb, i_targl, i_springk):
		newspring = c_spring(self, i_ma, i_mb, i_targl, i_springk)
		self.register_obj(newspring)
		return newspring
	
	def make_wall(self, i_line):
		newwall = c_wall(self, i_line)
		self.register_obj(newwall)
		return newwall
	
	def register_obj(self, i_obj):
		self.bucket.append(i_obj)
		self.bucklen = len(self.bucket)
	
	def update(self):
		# update springs
		for i in range(0,self.bucklen):
			if isinstance(self.bucket[i], c_spring):
				self.bucket[i].update()
		
		# update nodes
		for i in range(0,self.bucklen):
			if isinstance(self.bucket[i], c_node):
				for w in range(0,self.bucklen):
					if isinstance(self.bucket[w], c_wall):
						self.bucket[w].act(self.bucket[i])
				self.bucket[i].vel *= self.friction
				self.bucket[i].accel += self.gravity_glob
				self.bucket[i].update()
				if (self.ground):
					if (self.bucket[i].pos[1] >= self.ground):
						self.bucket[i].pos[1] = self.ground
						self.bucket[i].vel[0] *= self.ground_friction
	
	def list_nodes(self):
		list = []
		for i in range(0,self.bucklen):
			if isinstance(self.bucket[i], c_node):
				list.append(self.bucket[i].pos)
		return list
	
	def list_springs(self):
		list = []
		for i in range(0,self.bucklen):
			if isinstance(self.bucket[i], c_spring):
				list.append([self.bucket[i].ma.pos, self.bucket[i].mb.pos])
		return list
	
	def list_walls(self):
		list = []
		for i in range(0,self.bucklen):
			if isinstance(self.bucket[i], c_wall):
				list.append(self.bucket[i].line)
		return list

class c_node:
	def __init__(self, i_master, i_mass, i_pos, i_vel):
		# note: not integer resistant
		self.master = i_master
		self.pos = numpy.array(i_pos)
		self.oldpos = numpy.array(self.pos)
		self.vel = numpy.array(i_vel)
		self.accel = numpy.zeros(2)
		self.mass = i_mass
	
	def push(self, force):
		self.accel += force/self.mass
	
	def update(self):
		self.oldpos = numpy.array(self.pos)
		
		self.vel += self.accel
		self.pos += self.vel
		
		self.accel = numpy.zeros(2)

class c_spring:
	def __init__(self, i_master, i_ma, i_mb, i_targl, i_springk):
		self.master = i_master
		self.ma = i_ma
		self.mb = i_mb
		self.targl = float(i_targl)
		self.springk = float(i_springk)
	
	def update(self):
		diffv = numpy.array(self.mb.pos - self.ma.pos)
		length = numpy.linalg.norm(diffv)
		forcea = -1*self.springk*(self.targl - length) * (diffv / length)
		forceb = -1*forcea
		self.ma.push(forcea)
		self.mb.push(forceb)

class c_wall:
	def __init__(self, i_master, i_line):
		self.master = i_master
		self.line = i_line
		self.stunned = []
	
	def act(self, obj):
		for i in range(0,len(self.stunned)):
			if obj == self.stunned[i]:
				self.stunned.remove(obj)
				return
		x1 = obj.oldpos[0]
		y1 = obj.oldpos[1]
		x2 = obj.pos[0]
		y2 = obj.pos[1]
		
		u1 = self.line[0,0]
		v1 = self.line[0,1]
		u2 = self.line[1,0]
		v2 = self.line[1,1]
		
		b1 = (y2-y1)/(x2-x1)
		b2 = (v2-v1)/(u2-u1)
		
		a1 = y1-b1*x1
		a2 = v1-b2*u1
		
		xi = - (a1-a2)/(b1-b2)
		yi = a1+b1*xi
		
		if (x1-xi)*(xi-x2) >= 0:
			if (u1-xi)*(xi-u2) >= 0:
				if (y1-yi)*(yi-y2) >= 0:
					if (v1-yi)*(yi-v2) >= 0:
						self.stunned.append(obj)
						self.stunned.append(obj)
						obj.accel += -2*obj.vel
		
