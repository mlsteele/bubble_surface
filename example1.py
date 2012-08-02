"""
Miles Steele
2010

Example implementation of Cake
"""

import time, pygame, sys
import cake

def render(lagged):
	# Graphics
	screen.fill((255, 255, 255))
	if lagged:
		pd.circle(screen, (255, 0, 0), (w/2, h/2), 30)
	
	drawsprings = master.list_springs()
	for dp1, dp2 in drawsprings:
		dp1 = [ int(dp1[0]), int(dp1[1]) ]
		dp2 = [ int(dp2[0]), int(dp2[1]) ]
		pd.line(screen, (125, 125, 125), dp1, dp2, 1)
	
	drawnodes = master.list_nodes()
	for dp1 in drawnodes:
		dp1 = [ int(dp1[0]), int(dp1[1]) ]
		pd.circle(screen, (0, 0, 0), dp1, 2)
	
	drawwalls = master.list_walls()
	for dp1, dp2 in drawwalls:
		dp1 = [ int(dp1[0]), int(dp1[1]) ]
		dp2 = [ int(dp2[0]), int(dp2[1]) ]
		pd.line(screen, (0, 0, 0), dp1, dp2, 2)
		
	pygame.display.flip()

def main():
	# global variables
	global screen, pd, master, w, h
	
	## Graphics Initialization
	w = 200
	h = 200
	screen = pygame.display.set_mode((w, h))
	pygame.display.set_caption("Cake Physics Engine")
	pd = pygame.draw
	
	## Setup Master
	master = cake.c_master(friction=.92, gravity_glob=[0., 150.], slip=.3)
	
	## Object Creation
	# physics sandbox
	na = master.make_node(1.0, [w-100., 10.], i_vel=[0.01, 0.])
	nb = master.make_node(1.0, [w-200., 200.])
	nc = master.make_node(1.0, [w-120., 130.])
	tmpk = 30.
	tmpd = 1.
	controlme = master.make_spring(na, nb, 90., tmpk, damp=tmpd)
	controlme2 = master.make_spring(na, nc, 90., tmpk, damp=tmpd)
	master.make_spring(nb, nc, 90., tmpk)
	master.make_node(1.0, [430,190])
	master.make_node(1.0, [300,190])
	master.make_node(1.0, [450,190])
	
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
	#master.make_node(1.0, n.array([525., 170.]))
	#master.make_node(1.0, n.array([575., 170.]))
	#master.make_node(1.0, n.array([580., 170.]))
	
	# test damp spring
	master.make_spring(master.make_node(10, [w/2, h-20]), master.make_node(10, [w/2, h-80]), 120, 100., damp=1)
	
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
					pass
				if event.unicode in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
					pass
			if event.type == pygame.MOUSEBUTTONDOWN:
				pass
		
		timestep = time.time() - time_last
		time_last = time.time()
		if master.update((time.time()-time_start)/timescale, max=.033) == False:
			lagged = True
		#	print "simtime\t" + str(master.simtime)
		#	print "time offset\t" + str((time.time() - time_start) - master.simtime)
		#	print "frame\t" + str(frame)
		#	print "step\t" + str(timestep)
				
		## Render
		# fps frames per second
		since_render = time.time() - last_render
		fps = 60.
		dectime = time.time() - int(time.time())
		if since_render >= 1/fps:
			render(lagged)
			lagged = False
			last_render = time.time()

if __name__ == '__main__':
	main()
