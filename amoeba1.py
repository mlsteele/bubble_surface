import math
import numpy
import random
import cake
import time
import pygame

# Graphics initiation
w = 500
h = 500
screen = pygame.display.set_mode((w, h))
pd = pygame.draw

master = cake.c_master(i_friction=.92)
na = master.make_node(1.0, numpy.array([20., 30.]), i_vel=numpy.array([0.01, 0.]))
nb = master.make_node(1.0, numpy.array([80., 200.]))
thaspring = master.make_spring(na, nb, 90., .02)

# circle of circle_res
circle_res = 8
circle_radius = 100
circle = []
#unit circle generation
for i in range(0,circle_res):
	posx = numpy.cos(i*2.0*math.pi/circle_res)
	posy = numpy.sin(i*2.0*math.pi/circle_res)
	circle.append(master.make_node(1.0, numpy.array([posx, posy])))
#mass transform
for i in range(0,circle_res):
	circle[i].pos *= circle_radius
	circle[i].pos += numpy.array([w/2, h/2])
#ring spring generator
for i in range(0,circle_res):
	length = numpy.linalg.norm(circle[i].pos - circle[i-1].pos)
	master.make_spring(circle[i], circle[i-1], float(length), .02)
#muscle generator
muscles = []


frame = -1
while True:
	frame += 1
#	print "\n"
	
	master.update()
	
	screen.fill((255, 255, 255))
	
	drawsprings = master.list_springs()
	for i in range(0,len(drawsprings)):
		pd.line(screen, (125, 125, 125), drawsprings[i][0], drawsprings[i][1], 1)

	drawnodes = master.list_nodes()
	for i in range(0,len(drawnodes)):
		pd.circle(screen, (0, 0, 0), drawnodes[i], 3)
	
	pygame.display.flip()
	
	# remember the timestep :/
	time.sleep(.1)
