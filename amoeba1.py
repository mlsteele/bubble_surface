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

master = cake.c_master(friction=.92, gravity_glob=numpy.array([0, 5000]), ground=False, slip=.6)

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


# AMOEBA
# human input
circle_res = 10
circle_radius = 100.
muscle_period = .4
muscle_amp = 80.
reinforcement = 3
musclek = 1000
treadk = 1000

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
for r in range(1,reinforcement+1):
	for i in range(0,circle_res):
		length = numpy.linalg.norm(circle[i].pos - circle[i-r].pos)
		master.make_spring(circle[i], circle[i-r], float(length), treadk)

# muscle generator
muscle_count = circle_res/2
muscles = []
muscle_length = circle_radius*2
#muscle_length = numpy.linalg.norm(circle[i].pos - circle[i-4].pos) # should be at least close
for i in range(0,muscle_count):
	muscles.append( master.make_spring(circle[i], circle[i-muscle_count], circle_radius*2, musclek) )

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
	for m in range(0,muscle_count):
		muscles[m].targl = muscle_amp * numpy.sin( (master.simtime/muscle_period) + (m*2*math.pi/muscle_count) )
		muscles[m].targl += muscle_length
	master.update(timestep)
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