import time, pygame, sys
import numpy as n

import cake, bubble

# format position vector
def fp(pos):
  return n.array([float(pos[0]), float(pos[1])])

def render(lagged):
   # Graphics
   screen.fill((255, 255, 255))
   if lagged:
      pd.circle(screen, (255, 0, 0), (w/2, h/2), 30)
   
   drawsprings = physenv.list_springs()
   for dp1, dp2 in drawsprings:
      dp1 = [ int(dp1[0]), int(dp1[1]) ]
      dp2 = [ int(dp2[0]), int(dp2[1]) ]
      pd.line(screen, (125, 125, 125), dp1, dp2, 1)
   
   drawnodes = physenv.list_nodes()
   for dp1 in drawnodes:
      dp1 = [ int(dp1[0]), int(dp1[1]) ]
      pd.circle(screen, (0, 0, 0), dp1, 2)
   
   drawwalls = physenv.list_walls()
   for dp1, dp2 in drawwalls:
      dp1 = [ int(dp1[0]), int(dp1[1]) ]
      dp2 = [ int(dp2[0]), int(dp2[1]) ]
      pd.line(screen, (0, 0, 0), dp1, dp2, 2)
      
   pygame.display.flip()

def make_tee(xs, ys):
   lines = [
      [fp([xs[0], ys[0]]), fp([xs[1], ys[0]])],
      [fp([xs[1], ys[0]]), fp([xs[1], ys[1]])],
      [fp([xs[2], ys[0]]), fp([xs[2], ys[1]])],
      [fp([xs[2], ys[0]]), fp([xs[3], ys[0]])] ]

   for (a, b) in lines:
      physenv.make_wall([a, b])

def main():
   # global variables
   global screen, pd, physenv, w, h
   
   ## Graphics Initialization
   w, h = 400, 400
   screen = pygame.display.set_mode((w, h))
   pygame.display.set_caption("Cake Physics Engine")
   pd = pygame.draw
   
   ## Setup physenv
   physenv = cake.c_master(friction=.3, gravity_glob=[0., 0.], slip=.3)
   
   ## Object Creation
   bubble_starts = [[w/2, h/2]]
   bubbles = [bubble.bubble(physenv, c, 500) for c in bubble_starts]
   bubbles[0].area *= 6

   # terrain
   # ground_wall = physenv.make_wall([(-200, h-20), (w+200, h-10)])
   # slope_wall = physenv.make_wall([(200, h-5), (400, h-50)])
   # slope_wall = physenv.make_wall([(120, 0), (140, h)])
   # physenv.make_wall([(400, h-50), (500, h)])
   # physenv.make_wall([(w-10, h),(w-100, 5)], 1.)

   bst10, bst11 = bubble_starts[0][0], bubble_starts[0][1]
   make_tee([bst10 - 80, bst10 - 18, bst10 + 18, bst10 + 80], [bst11 - 20, bst11 + 50])
   
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
      if physenv.update((time.time()-time_start)/timescale, max=.033) == False:
         lagged = True
      #  print "simtime\t" + str(physenv.simtime)
      #  print "time offset\t" + str((time.time() - time_start) - physenv.simtime)
      #  print "frame\t" + str(frame)
      #  print "step\t" + str(timestep)
            
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
