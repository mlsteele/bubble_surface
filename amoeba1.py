import math
import numpy
import random
import cake
import time
import pygame

# Graphics initiation
w = 1200
h = 250
screen = pygame.display.set_mode((w, h))
pd = pygame.draw

master = cake.c_master(friction=.92, gravity_glob=numpy.array([0, .4]), ground=(h-10), ground_friction=.2)
#ground_wall = master.make_wall(numpy.array([(0, h-5), (w, h-5)]))

# test cases
na = master.make_node(1.0, numpy.array([20., 30.]), i_vel=numpy.array([0.01, 0.]))
nb = master.make_node(1.0, numpy.array([80., 200.]))
thaspring = master.make_spring(na, nb, 90., .02)

# AMOEBA
# human input
circle_res = 3
circle_radius = 100.
muscle_period = 30.
muscle_amp = 80.

# setup
circle_res *= 2
circle = []

# unit circle generation
for i in range(0,circle_res):
	posx = numpy.cos(i*2.0*math.pi/circle_res)
	posy = numpy.sin(i*2.0*math.pi/circle_res)
	circle.append(master.make_node(1.0, numpy.array([posx, posy])))

# mass transform
for i in range(0,circle_res):
	circle[i].pos *= 100
	circle[i].pos += numpy.array([circle_radius+10, h/2])

# ring spring generator
for i in range(0,circle_res):
	length = numpy.linalg.norm(circle[i].pos - circle[i-1].pos)
	master.make_spring(circle[i], circle[i-1], float(length), .2)

# muscle generator
muscle_count = circle_res/2
muscles = []
muscle_length = circle_radius*2
#muscle_length = numpy.linalg.norm(circle[i].pos - circle[i-4].pos) # should be at least close
for i in range(0,muscle_count):
	muscles.append( master.make_spring(circle[i], circle[i-muscle_count], circle_radius*2, .2) )


frame = -1
while True:
	frame += 1
#	print "\n"
	
	for m in range(0,muscle_count):
		muscles[m].targl = muscle_amp * numpy.sin( (frame/muscle_period) + (m*2*math.pi/muscle_count) )
		muscles[m].targl += muscle_length
	
	master.update()
	
	# Graphics
	screen.fill((255, 255, 255))
	
	drawsprings = master.list_springs()
	for i in range(0,len(drawsprings)):
		pd.line(screen, (125, 125, 125), drawsprings[i][0], drawsprings[i][1], 1)

	drawnodes = master.list_nodes()
	for i in range(0,len(drawnodes)):
		pd.circle(screen, (0, 0, 0), drawnodes[i], 3)
	
	drawwalls = master.list_walls()
	for i in range(0,len(drawwalls)):
		pd.line(screen, (0, 0, 0), drawwalls[i][0], drawwalls[i][1], 2)
	
	pygame.display.flip()
	
	# remember the timestep :/
#	time.sleep(.1)
