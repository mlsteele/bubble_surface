"""
Cake Physics Engine

Miles Steele
2011
"""

import numpy
n = numpy
import math
import time


class c_master:
	def __init__(s, friction=1., gravity_glob=numpy.zeros(2), slip=1):
		# Holders
		s.nodes, s.springs, s.walls, s.bangles = [], [], [], []
		s.nodesLen, s.springsLen, s.wallsLen, s.banglesLen = 0, 0, 0, 0
		s.update_objects = []
		
		s.friction = float(friction)
		s.gravity_glob = s.float_array(gravity_glob)
		s.slip = float(slip)
		s.simtime = 0.
		s.lagged_time = 0.
	
	def make_node(self, i_mass, i_pos, i_vel=numpy.zeros(2)):
		i_mass = float(i_mass)
		i_pos = self.float_array(i_pos)
		i_vel = self.float_array(i_vel)
		newnode = c_node(self, i_mass, i_pos, i_vel)
		self.nodes.append(newnode)
		self.nodesLen += 1
		return newnode
	
	def make_spring(self, ma, mb, targl, i_springk, damp=0.):
		if targl == True:
			targl = numpy.abs(numpy.linalg.norm(ma.pos - mb.pos))
		newspring = c_spring(self, ma, mb, float(targl), float(i_springk), float(damp))
		self.springs.append(newspring)
		self.springsLen += 1
		return newspring
	
	def make_bangle(self, na, nb, nc, tangle, power):
		newbangle = c_bangle(self, na, nb, nc, float(tangle), float(power))
		self.bangles.append(newbangle)
		self.banglesLen += 1
		return newbangle
	
	def make_wall(self, i_line, slip=False):
		if map(len, i_line) != [2,2]:
			print "Line not created! Check array length."
			return False
		formed_line = numpy.zeros( (2,2) )
		formed_line[0] = self.float_array(i_line[0])
		formed_line[1] = self.float_array(i_line[1])
		newwall = c_wall(self, formed_line, slip)
		self.walls.append(newwall)
		self.wallsLen += 1
		return newwall
	
	def update(s, nowtime, max=False):
		last_timestep = nowtime - (s.simtime + s.lagged_time)
		lagged = False
		if max and (last_timestep >= max):
			s.lagged_time += (last_timestep-float(max))
#			print "JUMPED!\tproposed step: " +str(last_timestep) +"\ttimestep set to " + str(max) + "\tlag is now: " + str(s.lagged_time)
			print "WARN: physics jumped"
			last_timestep = float(max)
			lagged = True
		
		# update springs
		for spring in s.springs:
			spring.update()
		
		# update bangles
		for bangle in s.bangles:
			bangle.update()
		
		# update nodes w/ walls		
		for node in s.nodes:
			node.vel *= s.friction**last_timestep
			node.accel += s.gravity_glob
			node.update(last_timestep)
			# postmortem wall check
			for wall in s.walls:
				if wall.act(node): 
					node.update(last_timestep, wall=True)

		[obj.update(last_timestep) for obj in s.update_objects]
		
		# update simulation time
		s.simtime += last_timestep
		if lagged:
			return False
		else:
			return last_timestep

	def add_update_object(s, obj):
		s.update_objects.append(obj)
	
	def list_nodes(self):
		return (o.pos for o in self.nodes)
	
	def list_springs(self):
		return ( [o.ma.pos, o.mb.pos] for o in self.springs)
	
	def list_walls(self):
		return (o.line for o in self.walls)
	
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
	
	def update(self, timestep, wall=False):
		self.contact = True
		
		if wall != True:
			self.oldpos = numpy.array(self.pos)
			self.contact = False
		
		# Euler Integration
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
		
		# initialize length
		diffv = n.array(self.mb.pos - self.ma.pos)
		self.length = n.linalg.norm(diffv)

	
	def update(self):
		diffv = numpy.array(self.mb.pos - self.ma.pos)
		self.length = numpy.linalg.norm(diffv)
		forcea = -1*self.springk*(self.targl - self.length) * (diffv / self.length)
		forceb = -1*forcea
		
		self.ma.accel += forcea/self.ma.mass
		self.mb.accel += forceb/self.mb.mass
		
		# Damping
		parallel = self.mb.pos - self.ma.pos
		parallel = parallel/numpy.linalg.norm(parallel)
		veldif = self.mb.vel - self.ma.vel
		veldif = numpy.dot(veldif, parallel)*parallel
		veldif *= self.damp
		
		self.ma.vel += veldif*self.damp
		self.mb.vel -= veldif*self.damp

## UNSTABLE
class c_bangle:
	# pushes two outer nodes to be at a certain angle relative to a middle node
	
	def __init__(self, master, na, nb, nc, tangle, power):
		s = self
		s.master, s.na, s.nb, s.nc, s.tangle, s.power = master, na, nb, nc, tangle, power
	
	def update(self):
		s = self
		pi = n.pi
		
		# vectors from nb
		va = s.na.pos - s.nb.pos
		vc = s.nc.pos - s.nb.pos
		
		# lengths of vectors
		val = n.linalg.norm(va)
		vcl = n.linalg.norm(vc)
		
		# normalized
		van = va / val
		vcn = vc / vcl
		
		# push vectors (perp)
		apushv = n.array([-van[1], van[0]])
		cpushv = n.array([-vcn[1], vcn[0]])
		
		# find current angle between
		cangle = n.arctan2(vc[0], vc[1]) - n.arctan2(va[0], va[1])
#		print 'cangle', int( cangle/n.pi*180 )
		
		# find middle angle between
		mangle = ( n.arctan2(vc[0], vc[1]) + n.arctan2(va[0], va[1]) )/2
#		print 'mangle', int( mangle/n.pi*180 )
		
		# find angle difference
		dangle = s.tangle - cangle
		dangle %= 2*n.pi
		dangle -= n.pi
		
		forcea = apushv*dangle*s.power
		forcec = -cpushv*dangle*s.power
		s.na.accel += forcea/s.na.mass
		s.nc.accel += forcec/s.nc.mass
		s.nb.accel += (-1*(forcea+forcec)) /s.nb.mass # equal opposite reaction
		
#		print 'dangle', int( dangle/n.pi*180 )
#		print '\n'

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
