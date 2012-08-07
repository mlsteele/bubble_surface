"""
Bubble
-----------------
Limited physical modeling of a microfluidic bubble
with surface tension and area conservation
"""

import math
import numpy as n

import cake

# format position vector
def fp(pos):
  return n.array([float(pos[0]), float(pos[1])])

class bubble:
  def __init__(s, physenv, centroid, area):
    s.physenv = physenv
    s.area = float(area)
    s.dot_spacing = 5.0

    s._assemble(fp(centroid), area)

  def calc_perimeter(s):
    return sum(n.linalg.norm(b - a)
      for (a, b)
      in zip(s.nodes, s.nodes[1:] + s.nodes[0:1]))

  def calc_area(s):
    # http://stackoverflow.com/questions/451426/how-do-i-calculate-the-surface-area-of-a-2d-polygon
    return 0.5 * abs(sum(a.pos[0] * b.pos[1] - b.pos[0] * a.pos[1]
      for (a, b)
      in zip(s.nodes, s.nodes[1:] + s.nodes[0:1])))

  def update(s, dt):
    s._contract(dt)
    s._expand(dt)

  def _contract(s, dt):
    force_time = 800.
    for (a,b,c) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1], s.nodes[2:] + s.nodes[0:2]):
      b.accel += (a.pos + c.pos - 2 * b.pos) * force_time / b.mass * dt

  def _expand(s, dt):
    if s.calc_area() > s.area: return

    force_time = 10000.
    for (a,b,c) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1], s.nodes[2:] + s.nodes[0:2]):
      parallel = a.pos - c.pos
      pre_normal = fp([-parallel[1], parallel[0]])
      normal = pre_normal / n.linalg.norm(pre_normal)
      b.accel += normal * force_time / b.mass * dt

  def _assemble(s, centroid, area):
    rad = math.sqrt(area / n.pi)
    circumference = 2 * n.pi * rad

    ## generate nodes
    res = circumference / s.dot_spacing
    s.nodes = []
    for i in range(0, int(res)):
      pos = fp([ n.cos(i * 2.0 * n.pi / res),
                 n.sin(i * 2.0 * n.pi / res) ])
      # mass transform
      pos *= rad
      pos += centroid
      # node creation
      s.nodes.append(s.physenv.make_node(1, pos))

    # ## generate surface
    # s.surface = [s.physenv.make_spring(a, b, True, 100, 0.5)
    #   for (a,b) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1])]

    s.physenv.add_update_object(s)
