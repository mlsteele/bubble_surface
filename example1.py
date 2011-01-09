import numpy
import random
import cake
import time

master = cake.c_master(i_friction=.92)
na = master.make_node(1.0, numpy.array([0., 0.]), i_vel=numpy.array([0.01, 0.]))
nb = master.make_node(1.0, numpy.array([5., 0.]))
thaspring = master.make_spring(na, nb, 4., 0.01)

frame = -1
while True:
	frame += 1
	
	master.update()
	
	print "\n" + str(frame)
	print na.pos
	print nb.pos
	time.sleep(.1)
