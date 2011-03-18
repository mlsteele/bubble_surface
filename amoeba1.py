"""
Miles Steele
2010

Stage for amoeba + cake testing
"""

import time, pygame, sys, random
from math import pi
import cake, amoeba

def randColorBright():
	c = [0,0,0]
	jump = 20
	while (c[0] < 255-jump and c[1] < 255-jump and c[2] < 255-jump):
		c[random.choice([0,1,2])] += jump
	
	return (int(c[0]), int(c[1]), int(c[2]))

def render(mode, lagged):
	# Graphics
	screen.fill((255, 255, 255))
	if lagged:
		pd.circle(screen, (255, 0, 0), (w/2, h/2), 30)
	
	if mode == 'stick':
		drawsprings = master.list_springs()
		for dp1, dp2 in drawsprings:
			dp1 = [ int(dp1[0]), int(dp1[1]) ]
			dp2 = [ int(dp2[0]), int(dp2[1]) ]
			pd.line(screen, (125, 125, 125), dp1, dp2, 1)
		
		drawnodes = master.list_nodes()
		for dp1 in drawnodes:
			dp1 = [ int(dp1[0]), int(dp1[1]) ]
			pd.circle(screen, (0, 0, 0), dp1, 2)
	
	elif mode == 'solid':
		drawpoly = []
		for dp in master.list_nodes():
			dp = [ int(dp[0]), int(dp[1]) ]
			drawpoly.append(dp)
			
		pd.polygon(screen, dcBright, drawpoly)
		pd.polygon(screen, (0,0,0), drawpoly, 2)
		
	drawwalls = master.list_walls()
	for dp1, dp2 in drawwalls:
		dp1 = [ int(dp1[0]), int(dp1[1]) ]
		dp2 = [ int(dp2[0]), int(dp2[1]) ]
		pd.line(screen, (0, 0, 0), dp1, dp2, 2)
		
	pygame.display.flip()

def main():
	# global variables
	global screen, pd, master, w, h, dcBright
	
	## Graphics Initialization
	w = 1200
	h = 250
	screen = pygame.display.set_mode((w, h))
	pygame.display.set_caption("Amoebas")
	pd = pygame.draw
	drawmode = 'stick'
	dcBright = randColorBright()
	
	master = cake.c_master(friction=.92, gravity_glob=[0., 150.], slip=.3)
	
	amoebas = []
	
	amoeba0 = amoeba.amoeba(master, [100, h-80])
	amoeba0.circle_res = 14
	amoeba0.circle_radius = 50.
	amoeba0.node_mass = 1.0
	amoeba0.treading = 3
	amoeba0.treadk = 100.
	amoeba0.tread_damp = .5
	amoeba0.musclek = 100
	amoeba0.muscle_period = .2*2*pi
	amoeba0.muscle_amp = 50.
	amoeba0.muscle_damp = .5
	
	amoeba1 = amoeba.amoeba(master, [100, h-80])
	amoeba1.circle_res = 20
	amoeba1.circle_radius = 50.
	amoeba1.node_mass = 1.0
	amoeba1.treading = 2
	amoeba1.treadk = 200.
	amoeba1.tread_damp = .5
	amoeba1.musclek = 400
	amoeba1.muscle_period = 1.2
	amoeba1.muscle_amp = 60.
	amoeba1.muscle_damp = .9
	
	amoeba2 = amoeba.amoeba(master, [150, h-70])
	amoeba2.circle_res = 14
	amoeba2.circle_radius = 20.
	amoeba2.node_mass = 1.
	amoeba2.treading = 2
	amoeba2.treadk = 100.
	amoeba2.tread_damp = .9
	amoeba2.musclek = 400.
	amoeba2.muscle_period = .7
	amoeba2.muscle_amp = 30.
	amoeba2.muscle_damp = amoeba2.tread_damp
	
	amoeba3 = amoeba.amoeba(master, [100, h-80])
	amoeba3.circle_res = 8
	amoeba3.circle_radius = 50.
	amoeba3.node_mass = 1.0
	amoeba3.treading = 2
	amoeba3.treadk = 200.
	amoeba3.tread_damp = .5
	amoeba3.musclek = 400
	amoeba3.muscle_period = .2*2*pi
	amoeba3.muscle_amp = 60.
	amoeba3.muscle_damp = .9
	
	amoeba4 = amoeba.amoeba(master, [100, h-80])
	amoeba4.circle_res = 10
	amoeba4.circle_radius = 50.
	amoeba4.node_mass = 1.0
	amoeba4.treading = 2
	amoeba4.treadk = 200.
	amoeba4.tread_damp = .5
	amoeba4.musclek = 400
	amoeba4.muscle_period = .18*2*pi
	amoeba4.muscle_amp = 90.
	amoeba4.muscle_damp = .9
	
	amoebas.append(amoeba0)
	amoebas.append(amoeba1)
	amoebas.append(amoeba2)
	amoebas.append(amoeba3)
	amoebas.append(amoeba4)
	
	activeID = 2
	amoebas[activeID].assemble()
	
	"""
	# physics sandbox
	na = master.make_node(1.0, [w-100., 10.], i_vel=[0.01, 0.])
	nb = master.make_node(1.0, [w-200., 200.])
	nc = master.make_node(1.0, [w-120., 130.])
	tmpk = 30.
	tmpd = 1.
	controlme = master.make_spring(na, nb, 90., tmpk, damp=tmpd)
	controlme2 = master.make_spring(na, nc, 90., tmpk, damp=tmpd)
	master.make_spring(nb, nc, 90., tmpk)
	master.make_node(1.0, numpy.array([430,190]))
	master.make_node(1.0, numpy.array([300,190]))
	master.make_node(1.0, numpy.array([450,190]))
	
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
	"""
	
	# terrain
	ground_wall = master.make_wall([(-200, h-20), (w+200, h-10)])
	slope_wall = master.make_wall([(200, h-5), (400, h-50)])
	master.make_wall([(400, h-50), (500, h)])
	master.make_wall([(w-10, h),(w-100, 5)], 1.)
	
	timescale = 1
	timestep = time.time()
	time_last = time.time()
	time_start = time.time()
	last_render = 0.
	lagged = False
	frame = -1
	while True:
		frame += 1
		
		## Event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit(); sys.exit();
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.unicode == 'q':
					pygame.quit(); sys.exit();
				if event.key == pygame.K_SPACE:
					dcBright = randColorBright()
					if drawmode == 'stick':
						drawmode = 'solid'
					elif drawmode == 'solid':
						drawmode = 'stick'
				if event.unicode in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
					if int(event.unicode) in range(1,len(amoebas)+1):
						dcBright = randColorBright()
						amoebas[activeID].destroy()
						activeID = int(event.unicode)-1
						amoebas[activeID].assemble()
						print "amoeba ID:\t", activeID
			if event.type == pygame.MOUSEBUTTONDOWN:
				amoebas[activeID].destroy()
				activeID = (activeID + 1) % len(amoebas)
				amoebas[activeID].assemble()
				dcBright = randColorBright()
				print "amoeba ID:\t", activeID
		
		timestep = time.time() - time_last
		time_last = time.time()
		if master.update((time.time()-time_start)/timescale, max=.033) == False:
			lagged = True
		#	print "simtime\t" + str(master.simtime)
		#	print "time offset\t" + str((time.time() - time_start) - master.simtime)
		#	print "frame\t" + str(frame)
		#	print "step\t" + str(timestep)
		
		## Update
		amoebas[activeID].update(master.timestep)
		
		## Win Test
		if amoebas[activeID].circle[0].pos[0] >= w-150:
			amoebas[activeID].destroy()
			activeID = (activeID + 1) % len(amoebas)
			amoebas[activeID].assemble()
			dcBright = randColorBright()
			print "amoeba ID:\t", activeID
				
		## Render
		# fps frames per second
		since_render = time.time() - last_render
		fps = 60.
		dectime = time.time() - int(time.time())
		if since_render >= 1/fps:
			render(drawmode, lagged)
			lagged = False
			last_render = time.time()

if __name__ == '__main__':
	main()