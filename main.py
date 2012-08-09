import time, pygame, sys
import numpy as n

import cake, bubble

# format position vector
def fp(pos):
  return n.array([float(pos[0]), float(pos[1])])

def render():
   # Graphics
   screen.fill((255, 255, 255))
   
   drawsprings = physenv.list_springs()
   for dp1, dp2 in drawsprings:
      dp1 = [ int(dp1[0]), int(dp1[1]) ]
      dp2 = [ int(dp2[0]), int(dp2[1]) ]
      pd.line(screen, (125, 125, 125), dp1, dp2, 1)
   
   render_as_solid = True

   if render_as_solid:
      for bubble in bubbles:
         poly = bubble.get_polygon()
         pd.polygon(screen, (106, 208, 223), poly)
         pd.polygon(screen, (0, 0, 0), poly, 1)
   else:
      drawnodes = physenv.list_nodes()
      for dp1 in drawnodes:
         dp1 = [ int(dp1[0]), int(dp1[1]) ]
         pd.circle(screen, (100, 100, 100), dp1, 2)

   drawwalls = physenv.list_walls()
   for dp1, dp2 in drawwalls:
      dp1 = [ int(dp1[0]), int(dp1[1]) ]
      dp2 = [ int(dp2[0]), int(dp2[1]) ]
      pd.line(screen, (0, 0, 0), dp1, dp2, 2)
      
   pygame.display.flip()

def handle_common_events(handler=None):
   ## Event handler
   for event in pygame.event.get():
      if handler and not handler(event):
         if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.unicode == 'q':
               pygame.quit(); sys.exit();

def make_tee(xs, ys):
   [physenv.make_wall([a, b]) for (a, b)
   in [[[xs[0], ys[0]], [xs[1], ys[0]]],
       [[xs[1], ys[0]], [xs[1], ys[1]]],
       [[xs[2], ys[0]], [xs[2], ys[1]]],
       [[xs[2], ys[0]], [xs[3], ys[0]]] ]]

def make_wye(org, channelWidth, theta): #org is the center point of the junction. theta is angle below horizontal x axis
  def w(a, b):
    physenv.make_wall([a,b])
  org, channelWidth, theta = fp(org), float(channelWidth), float(theta)
  channelHeightMult = 10
  channelHeight = channelWidth*channelHeightMult
  junctionYLoc = channelHeight/2
  yU = junctionYLoc - channelWidth/2
  yL = yU + channelWidth/n.cos(theta)
  offshootXDistance = channelHeight/4
  offshootXEnd = offshootXDistance +channelWidth
  yLEndPoint = n.tan(theta)*(offshootXEnd - channelWidth)+yL
  yUEndPoint = n.tan(theta)*(offshootXEnd - channelWidth)+yU
  org = org - [channelWidth/2,channelHeight/2]
  point1 = org
  point2 = org + [0,channelHeight]
  point3 = org + [channelWidth, channelHeight]
  point4 = org + [channelWidth, yL]
  point5 = org + [offshootXEnd, yLEndPoint]
  point6 = org + [offshootXEnd, yUEndPoint]
  point7 = org + [channelWidth, yU]
  point8 = org + [channelWidth, 0]
  w(point1, point2)
  w(point2, point3)
  w(point3, point4)
  w(point4,point5)
  w(point5,point6)
  w(point6,point7)
  w(point7,point8)
  w(point8,point1)
  

def make_ray_channel(centroid, angle, rad, length):
   centroid, angle, rad, length = fp(centroid), float(angle), float(rad), float(length)
   def fa(ang): return fp([n.cos(ang), n.sin(ang)])   
   centroid2 = centroid + fa(angle) * length
   wp = [fa(angle + n.pi * 0.5) * rad, fa(angle + n.pi * 1.5) * rad]
   physenv.make_wall([wp[0] + centroid, wp[0] + centroid2])
   physenv.make_wall([wp[1] + centroid, wp[1] + centroid2])

def make_tri_channels(centroid, angles):
   centroid, angles = fp(centroid), [float(a) for a in angles]
   [make_ray_channel(centroid, a, 10, 100) for a in angles]


def info_on_click(e):
   if e.type == pygame.MOUSEBUTTONDOWN:
      bubbles[0].print_info()

def run_continuous():
   time_stack = 0.
   time_stack_last = time.time()
   time_step = 0.033
   timescale = time_step / 0.03
   last_render = 0.
   fps_max = 50.
   fps_min = 50.
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
            [b.print_info() for b in bubbles]
      
      time_stack += (time.time() - time_stack_last) * timescale
      # time_stack += time_step
      time_stack_last = time.time()
      frame_calc_start = time.time()
      while time_stack >= time_step:
         physenv.update(time_step)
         time_stack -= time_step
         if time.time() - frame_calc_start > 1/fps_min:
            break
      #  print "simtime\t" + str(physenv.simtime)
      #  print "time offset\t" + str((time.time() - time_start) - physenv.simtime)
      #  print "frame\t" + str(frame)
      #  print "step\t" + str(timestep)
            
      ## Render
      # fps frames per second
      since_render = time.time() - last_render
      dectime = time.time() - int(time.time())
      if since_render >= 1/fps_max:
         render()
         last_render = time.time()

def run_until_condition():
   [physenv.update(0.033) for x in range(0,10)]
   while not bubbles[0].has_settled():
      handle_common_events(info_on_click)
      physenv.update(0.033)

   render()

   while True:
      handle_common_events(info_on_click)

def main():
   # global variables
   global screen, pd, physenv, w, h, bubbles
   
   ## Graphics Initialization
   w, h = 400, 400
   screen = pygame.display.set_mode((w, h))
   pygame.display.set_caption("Bubble")
   pd = pygame.draw
   
   ## Setup physenv
   grav_dir_index = 0
   physenv = cake.c_master(friction=.3, gravity_glob=[0., [0, 50, -50.][grav_dir_index]], slip=0.0)
   
   ## Bubbles
   bubble_starts = [[w/2, h/2 + [0, -100, 100][grav_dir_index]]]
   bubbles = [bubble.bubble(physenv, c, 500) for c in bubble_starts]
   bubbles[0].area *= 6

   ## Walls
   c42 = [w/2,h/2-30]
   make_wye(org = c42, channelWidth = 30, theta = n.pi/5)

   [run_continuous, run_until_condition][0]()

if __name__ == '__main__':
   main()
