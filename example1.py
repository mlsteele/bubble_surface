import numpy
import random
import cake

master = cake.c_master()
na = master.make_node(1, numpy.array([0, 0]), i_vel=numpy.array([1, 0]))
nb = master.make_node(1, numpy.array([5, 0]))

frame = -1
while True:
	frame += 1
	
