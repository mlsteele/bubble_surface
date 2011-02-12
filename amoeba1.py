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

master = cake.c_master(friction=.92, gravity_glob=[0., 150.], slip=.3)

amoebas = []

amoeba1 = amoeba.amoeba(master, [100, h-80])
amoeba1.circle_res = 7
amoeba1.circle_radius = 50.
amoeba1.node_mass = 1.0
amoeba1.treading = 3
amoeba1.treadk = 100.
amoeba1.tread_damp = .5
amoeba1.musclek = 100
amoeba1.muscle_period = .2*2*math.pi
amoeba1.muscle_amp = 50.
amoeba1.muscle_damp = .5

amoeba2 = amoeba.amoeba(master, [100, h-80])
amoeba2.circle_res = 10
amoeba2.circle_radius = 50.
amoeba2.node_mass = 1.0
amoeba2.treading = 1
amoeba2.treadk = 200.
amoeba2.tread_damp = .5
amoeba2.musclek = 400
amoeba2.muscle_period = 1.2
amoeba2.muscle_amp = 60.
amoeba2.muscle_damp = .9

amoeba3 = amoeba.amoeba(master, [150, h-70])
amoeba3.circle_res = 7
amoeba3.circle_radius = 20.
amoeba3.node_mass = 1.
amoeba3.treading = 2
amoeba3.treadk = 100.
amoeba3.tread_damp = .9
amoeba3.musclek = 400.
amoeba3.muscle_period = .05
amoeba3.muscle_amp = 30.
amoeba3.muscle_damp = amoeba3.tread_damp

amoeba4 = amoeba.amoeba(master, [100, h-80])
amoeba4.circle_res = 4
amoeba4.circle_radius = 50.
amoeba4.node_mass = 1.0
amoeba4.treading = 2
amoeba4.treadk = 200.
amoeba4.tread_damp = .5
amoeba4.musclek = 400
amoeba4.muscle_period = .2*2*math.pi
amoeba4.muscle_amp = 60.
amoeba4.muscle_damp = .9

amoeba5 = amoeba.amoeba(master, [100, h-80])
amoeba5.circle_res = 5
amoeba5.circle_radius = 50.
amoeba5.node_mass = 1.0
amoeba5.treading = 2
amoeba5.treadk = 200.
amoeba5.tread_damp = .5
amoeba5.musclek = 400
amoeba5.muscle_period = .18*2*math.pi
amoeba5.muscle_amp = 90.
amoeba5.muscle_damp = .9

#amoebas.append(amoeba1)
#amoeba1.assemble()

#amoebas.append(amoeba2)
#amoeba2.assemble()

amoebas.append(amoeba3)
amoeba3.assemble()

#amoebas.append(amoeba4)
#amoeba4.assemble()

#amoebas.append(amoeba5)
#amoeba5.assemble()

# physics sandbox
na = master.make_node(1.0, [w-100., 10.], i_vel=[0.01, 0.])
nb = master.make_node(1.0, [w-200., 200.])
nc = master.make_node(1.0, [w-120., 130.])
tmpk = 30.
tmpd = 1.
controlme = master.make_spring(na, nb, 90., tmpk, damp=tmpd)
controlme2 = master.make_spring(na, nc, 90., tmpk, damp=tmpd)
master.make_spring(nb, nc, 90., tmpk)
#master.make_node(1.0, numpy.array([430,190]))
#master.make_node(1.0, numpy.array([300,190]))
#master.make_node(1.0, numpy.array([450,190]))
master.make_wall([(w-10, h),(w-100, 5)], 1.)
ground_wall = master.make_wall([(-200, h-20), (w+200, h-10)])

# terrain
slope_wall = master.make_wall([(200, h-5), (400, h-50)])
master.make_wall([(400, h-50), (500, h)])

# test slip spring
master.make_wall([((w/2)-100.,50.),((w/2)+40.,30.)], slip=1.)
tna = master.make_node(1.0, [w/2.,20.])
tnb = master.make_node(1.0, [(w/2)+2.,60.])
master.make_spring(tna, tnb, 41., 50., damp=1.)
ttna = master.make_node(1.0, [w/2+20.,15.])
ttnb = master.make_node(1.0, [(w/2+20)+2.,55.])
master.make_spring(ttna, ttnb, 41., 50., damp=0.)
independent_node = master.make_node(1.0, [w/2+10.,20.])

# test slip spring 2
#master.make_wall([(500.,200.),(550.,170.)], slip=1.)
#master.make_wall([(550.,170.),(600.,200.)], slip=1.)
#master.make_node(1.0, numpy.array([525., 170.]))
#master.make_node(1.0, numpy.array([575., 170.]))
#master.make_node(1.0, numpy.array([580., 170.]))

# test damp spring
master.make_spring(master.make_node(10, [w/2, h-20]), master.make_node(10, [w/2, h-80]), 120, 100., damp=1)

def render(lagged):
	# Graphics
	screen.fill((255, 255, 255))
	if lagged:
		pd.circle(screen, (255, 0, 0), (w/2, h/2), 30)
	
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

timescale = 1
timestep = time.time()
time_last = time.time()
time_start = time.time()
last_render = 0.
lagged = False
frame = -1
while True:
	frame += 1
#	print "\n"
	
	timestep = time.time() - time_last
	time_last = time.time()
	if master.update((time.time()-time_start)/timescale, max=.033) == False:
		lagged = True
	for a in range(0,len(amoebas)):
		amoebas[a].update(master.timestep)
#	print "simtime\t" + str(master.simtime)
#	print "time offset\t" + str((time.time() - time_start) - master.simtime)
#	print "frame\t" + str(frame)
#	print "step\t" + str(timestep)
	
	# render fps frames per second
	since_render = time.time() - last_render
	fps = 60.
	dectime = time.time() - int(time.time())
	if since_render >= 1/fps:
		render(lagged)
		lagged = False
		last_render = time.time()
	
	# remember the timestep :/
#	time.sleep(1./1000)