import math
import numpy
import random
import time
import pygame

import cake
import amoeba

# Graphics initiation
w = 1200
h = 250
screen = pygame.display.set_mode((w, h))
pd = pygame.draw

master = cake.c_master(friction=.92, gravity_glob=numpy.array([0, 5000]), ground=False, slip=.6)

amoebas = []
amoeba1 = amoeba.amoeba(master, numpy.array([200, h/2]))
amoeba1.circle_res = 8
amoeba1.circle_radius = 50.
amoeba1.node_mass = 1.0
amoeba1.treading = 3
amoeba1.treadk = 1000.
amoeba1.musclek = 1000.
amoeba1.muscle_period = .2
amoeba1.muscle_amp = 50.
amoeba2 = amoeba.amoeba(master, numpy.array([200, h/2]))
amoeba2.circle_res = 10
amoeba2.circle_radius = 50.
amoeba2.node_mass = .2
amoeba2.treading = 1
amoeba2.treadk = 1000.
amoeba2.musclek = 500.
amoeba2.muscle_period = .3
amoeba2.muscle_amp = 40.

amoebas.append(amoeba1)
amoeba1.assemble()
#amoebas.append(amoeba2)
#amoeba2.assemble()


# physics sandbox
na = master.make_node(1.0, numpy.array([w-100., 10.]), i_vel=numpy.array([0.01, 0.]))
nb = master.make_node(1.0, numpy.array([w-200., 200.]))
nc = master.make_node(1.0, numpy.array([w-120., 130.]))
tmpk = 1000
controlme = master.make_spring(na, nb, 90., tmpk)
controlme2 = master.make_spring(na, nc, 90., tmpk)
master.make_spring(nb, nc, 90., tmpk)
slope_wall = master.make_wall(numpy.array([(200, h-5), (400, h-50)]))
master.make_wall(numpy.array([(400, h-50), (500, h)]))
master.make_wall(numpy.array([(w-100, 5), (w-10, h)]))
ground_wall = master.make_wall(numpy.array([(-200, h-20), (w+200, h-10)]))

def render():
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
	
#	drawpaths = master.list_paths()
#	for i in range(0,len(drawpaths)):
#		pd.line(screen, (255, 0, 0), drawpaths[i][0], drawpaths[i][1], 1)
	
	pygame.display.flip()

timestep = time.time()
last_render = 0.
frame = -1
while True:
	frame += 1
#	print "\n"
	
	timestep = time.time() - timestep
	for a in range(0,len(amoebas)):
		amoebas[a].update(master.simtime)
	master.update(timestep*1.2)
	timestep = time.time()
	
	# render fps frames per second
	since_render = time.time() - last_render
	fps = 60.
	dectime = time.time() - int(time.time())
	if since_render >= 1/fps:
		render()
		last_render = time.time()
	
	# remember the timestep :/
#	time.sleep(1./1000)