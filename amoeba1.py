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
	if lagged:
		pd.circle(screen, (255, 0, 0), (w/2, h/2), 30)
	
	drawwalls = master.list_walls()
	for dp1, dp2 in drawwalls:
		dp1 = [ int(dp1[0]), int(dp1[1]) ]
		dp2 = [ int(dp2[0]), int(dp2[1]) ]
		pd.line(screen, (0, 0, 0), dp1, dp2, 2)
	
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
	
	master = cake.c_master(friction=.92, gravity_glob=[0., 200.], slip=.8)
	
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
	
	amoeba5 = amoeba.amoeba(master, [100, h-180])
	amoeba5.circle_res = 16
	amoeba5.circle_radius = 30.
	amoeba5.node_mass = 1.0
	amoeba5.treading = 2
	amoeba5.treadk = 600.
	amoeba5.tread_damp = .5
	amoeba5.musclek = 40
	amoeba5.muscle_period = .18*2*pi
	amoeba5.muscle_amp = 20.
	amoeba5.muscle_damp = .2
	
#	amoebas.append(amoeba0)
#	amoebas.append(amoeba1)
#	amoebas.append(amoeba2)
#	amoebas.append(amoeba3)
#	amoebas.append(amoeba4)
	amoebas.append(amoeba5)
	
	activeID = 0
	amoebas[activeID].assemble()
	
	# terrain
	ground_wall = master.make_wall([(-200, h-20), (w+200, h-10)])
	slope_wall = master.make_wall([(200, h-5), (400, h-50)])
	master.make_wall([(400, h-50), (500, h)])
	
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
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.unicode == 'q':
					pygame.quit(); sys.exit();
				elif event.key == pygame.K_v:
					dcBright = randColorBright()
					if drawmode == 'stick':
						drawmode = 'solid'
					elif drawmode == 'solid':
						drawmode = 'stick'
				elif event.unicode in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
					if int(event.unicode) in range(1,len(amoebas)+1):
						dcBright = randColorBright()
						amoebas[activeID].destroy()
						activeID = int(event.unicode)-1
						amoebas[activeID].assemble()
						print "amoeba ID:\t", activeID
				elif event.key == pygame.K_RIGHT:
					amoebas[activeID].control.right = True
				elif event.key == pygame.K_LEFT:
					amoebas[activeID].control.left = True
				elif event.key == pygame.K_DOWN:
					amoebas[activeID].control.down = True
				elif event.key == pygame.K_UP:
					amoebas[activeID].control.up = True
				elif event.key == pygame.K_SPACE:
					amoebas[activeID].control.poof = True
#				elif event.key == pygame.K_s:
#					master.slip = .99
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					amoebas[activeID].control.right = False
				elif event.key == pygame.K_LEFT:
					amoebas[activeID].control.left = False
				elif event.key == pygame.K_DOWN:
					amoebas[activeID].control.down = False
				elif event.key == pygame.K_UP:
					amoebas[activeID].control.up = False
				elif event.key == pygame.K_SPACE:
					amoebas[activeID].control.poof = False
#				elif event.key == pygame.K_s:
#					master.slip = .8
			elif event.type == pygame.MOUSEBUTTONDOWN:
				amoebas[activeID].destroy()
				activeID = (activeID + 1) % len(amoebas)
				amoebas[activeID].assemble()
				dcBright = randColorBright()
				print "amoeba ID:\t", activeID
		
		## Time Steppage
		timestep = time.time() - time_last
		time_last = time.time()
		if master.update((time.time()-time_start)*timescale, max=.033) == False:
			lagged = True
		#	print "simtime\t" + str(master.simtime)
		#	print "time offset\t" + str((time.time() - time_start) - master.simtime)
		#	print "frame\t" + str(frame)
		#	print "step\t" + str(timestep)
		
		## Update Amoeba
		amoebas[activeID].update(master.timestep)
		
		# Win Test
		if amoebas[activeID].circle[0].pos[0] >= w-15:
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
			screen.fill((255, 255, 255))
			render(drawmode, lagged)
			pygame.display.flip()
			lagged = False
			last_render = time.time()

if __name__ == '__main__':
	main()