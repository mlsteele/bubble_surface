import numpy
import math
import time

class c_master:
	def __init__(self, friction=1., gravity_glob=numpy.zeros(2), ground=False, slip=1):
		self.bucket = []
		self.bucklen = 0
		
		self.friction = friction
		self.gravity_glob = gravity_glob
		self.ground = ground
		self.slip = slip
		self.simtime = 0.
	
	def make_node(self, i_mass, i_pos, i_vel=numpy.zeros(2)):
		newnode = c_node(self, i_mass, i_pos, i_vel)
		self.register_obj(newnode)
		return newnode
	
	def make_spring(self, i_ma, i_mb, i_targl, i_springk):
		newspring = c_spring(self, i_ma, i_mb, i_targl, i_springk)
		self.register_obj(newspring)
		return newspring
	
	def make_wall(self, i_line, slip=False):
		newwall = c_wall(self, i_line, slip)
		self.register_obj(newwall)
		return newwall
	
	def register_obj(self, i_obj):
		self.bucket.append(i_obj)
		self.bucklen = len(self.bucket)
	
	def update(self, timestep):
		# update springs
		for i in range(0,self.bucklen):
			if isinstance(self.bucket[i], c_spring):
				self.bucket[i].update()
		
		# update nodes
		for i in range(0,self.bucklen):
			if isinstance(self.bucket[i], c_node):
				self.bucket[i].vel *= self.friction
				self.bucket[i].accel += self.gravity_glob
				self.bucket[i].update(timestep)
				# hard collisions
				if (self.ground):
					if (self.bucket[i].pos[1] >= self.ground):
						self.bucket[i].pos[1] = self.ground
						self.bucket[i].vel[0] *= self.slip
				for w in range(0,self.bucklen):
					if isinstance(self.bucket[w], c_wall):
						self.bucket[w].act(self.bucket[i])
		self.simtime += timestep
	
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
	
	def list_paths(self):
		list = []
		for i in range(0,self.bucklen):
			if isinstance(self.bucket[i], c_node):
				list.append([self.bucket[i].pos, self.bucket[i].oldpos])
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
	
	def update(self, timestep):
		self.oldpos = numpy.array(self.pos)
		
		self.vel += self.accel * timestep
		self.pos += self.vel * timestep
		
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
	def __init__(self, i_master, i_line, i_slip):
		self.master = i_master
		self.line = i_line
		if i_slip:
			self.slip = i_slip
		else:
			self.slip = self.master.slip
	
	def act(self, obj):
		# lines A-B, C-D
		A = obj.oldpos
		x1 = obj.oldpos[0]
		y1 = obj.oldpos[1]
		
		B = obj.pos
		x2 = obj.pos[0]
		y2 = obj.pos[1]
		
		C = self.line[0,0:2]
		u1 = self.line[0,0]
		v1 = self.line[0,1]
		
		D = self.line[1,0:2]
		u2 = self.line[1,0]
		v2 = self.line[1,1]
		
		def ccw(A,B,C):
			return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

		def intersect(A,B,C,D):
			return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
		
		xsect_bool = intersect(A,B,C,D)
		if xsect_bool != True:
			return
		
		obj.pos = numpy.array(obj.oldpos)
		parallel = (self.line[1]-self.line[0])
		parallel = parallel / numpy.linalg.norm(parallel)
#		obj.vel = numpy.dot(obj.vel,parallel)
#		obj.vel *= self.slip
