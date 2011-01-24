import numpy
import math
import time

class c_master:
	def __init__(self, friction=1., gravity_glob=numpy.zeros(2), slip=1):
		self.bucket = []
		self.bucklen = 0
		
		self.friction = float(friction)
		self.gravity_glob = self.float_array(gravity_glob)
		self.slip = float(slip)
		self.simtime = 0.
		self.lag = 0.
		self.timestep = 0.
	
	def make_node(self, i_mass, i_pos, i_vel=numpy.zeros(2)):
		i_mass = float(i_mass)
		i_pos = self.float_array(i_pos)
		i_vel = self.float_array(i_vel)
		newnode = c_node(self, i_mass, i_pos, i_vel)
		self.register_obj(newnode)
		return newnode
	
	def make_spring(self, ma, mb, targl, i_springk, damp=0.):
		if targl == True:
			targl = numpy.abs(numpy.linalg.norm(ma.pos - mb.pos))
		newspring = c_spring(self, ma, mb, float(targl), float(i_springk), float(damp))
		self.register_obj(newspring)
		return newspring
	
	def make_wall(self, i_line, slip=False):
		if map(len, i_line) != [2,2]:
			print "Line not created! Check array length."
			return False
		formed_line = numpy.zeros( (2,2) )
		formed_line[0] = self.float_array(i_line[0])
		formed_line[1] = self.float_array(i_line[1])
		newwall = c_wall(self, formed_line, slip)
		self.register_obj(newwall)
		return newwall
	
	def register_obj(self, i_obj):
		self.bucket.append(i_obj)
		self.bucklen = len(self.bucket)
	
	def update(self, nowtime, max=False):
		self.timestep = nowtime - (self.simtime + self.lag)
		lagged = False
		if self.timestep >= max:
			self.lag += (self.timestep-float(max))
			print "JUMPED!\tproposed step: " +str(self.timestep) +"\ttimestep set to " + str(max) + "\tlag is now: " + str(self.lag)
			self.timestep = float(max)
			lagged = True
		
		# update springs
		for i in range(0,self.bucklen):
			if isinstance(self.bucket[i], c_spring):
				self.bucket[i].update(self.timestep)
		
		# update nodes w/ walls
		for i in range(0,self.bucklen):
			if isinstance(self.bucket[i], c_node):
				self.bucket[i].vel *= self.friction**self.timestep
				self.bucket[i].accel += self.gravity_glob
				self.bucket[i].update(self.timestep)
				# postmortem wall check
				for w in range(0,self.bucklen):
					if isinstance(self.bucket[w], c_wall):
						if self.bucket[w].act(self.bucket[i]): 
							self.bucket[i].update(self.timestep, wall=True)
		
		# update simulation time
		self.simtime += self.timestep
		if lagged:
			return False
		else:
			return self.timestep
	
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
				list.append([self.bucket[i].goal, self.bucket[i].pos])
		return list
	
	def float_array(self, ia):
		oa = numpy.zeros(len(ia))
		for i in range(0,len(ia)):
			oa[i] = ia[i]
		return oa

class c_node:
	def __init__(self, i_master, i_mass, i_pos, i_vel):
		# note: not integer resistant
		self.master = i_master
		self.pos = numpy.array(i_pos)
		self.oldpos = numpy.array(self.pos)
		self.vel = numpy.array(i_vel)
		self.accel = numpy.zeros(2)
		self.mass = i_mass
		self.contact = False
	
	def push(self, force):
		self.accel += force/self.mass
	
	def update(self, timestep, wall=False):
		self.contact = True
		if wall != True:
			self.oldpos = numpy.array(self.pos)
			self.contact = False
		
		self.vel += self.accel * timestep
		self.pos += self.vel * timestep
		
		#self.pos += .5 * self.accel * (timestep**2)
		#self.pos += self.vel * timestep
		#self.vel += self.accel * timestep
		
		self.accel = numpy.zeros(2)
		

class c_spring:
	def __init__(self, i_master, i_ma, i_mb, i_targl, i_springk, damp):
		self.master = i_master
		self.ma = i_ma
		self.mb = i_mb
		self.targl = float(i_targl)
		self.springk = float(i_springk)
		self.damp = damp
	
	def update(self, timestep):
		diffv = numpy.array(self.mb.pos - self.ma.pos)
		length = numpy.linalg.norm(diffv)
		forcea = -1*self.springk*(self.targl - length) * (diffv / length)
		forceb = -1*forcea
		
		self.ma.push(forcea)
		self.mb.push(forceb)
		
		# Damping
		parallel = self.mb.pos - self.ma.pos
		parallel = parallel/numpy.linalg.norm(parallel)
		veldif = self.mb.vel - self.ma.vel
		veldif = numpy.dot(veldif, parallel)*parallel
		veldif *= self.damp
		
		self.ma.vel += veldif*self.damp
		self.mb.vel -= veldif*self.damp

class c_wall:
	def __init__(self, i_master, i_line, i_slip):
		self.master = i_master
		self.line = i_line
		if i_slip:
			self.slip = i_slip
		else:
			self.slip = self.master.slip
		self.parallel = (self.line[1]-self.line[0])
		self.parallel = self.parallel / numpy.linalg.norm(self.parallel)
	
	def act(self, obj):
		# all this thanks to http://www.geog.ubc.ca/courses/klink/gis.notes/ncgia/u32.html#SEC32.3.5
		
		# lines A-B, C-D
		A = obj.oldpos
		x1 = A[0]
		y1 = A[1]
		
		B = obj.pos
		x2 = B[0]
		y2 = B[1]
		
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
			return False
		obj.pos = numpy.array(obj.oldpos)
		obj.vel = numpy.dot(obj.vel,self.parallel)*self.parallel
		obj.vel *= self.slip
		return True