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
    s.dot_spacing = 8.0
    s.node_proto_mass = 1

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
    # print "relative scaling %s" % (s.calc_area() / s.area)

    s._redistribute_surface()
    s._contract(dt)
    s._expand(dt)

  def _contract(s, dt):
    force_time = 800.
    for (a,b,c) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1], s.nodes[2:] + s.nodes[0:2]):
      b.accel += (a.pos + c.pos - 2 * b.pos) * force_time / b.mass * dt

  def _expand(s, dt):
    if s.calc_area() > s.area: return

    force_time = 6000.
    for (a,b,c) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1], s.nodes[2:] + s.nodes[0:2]):
      parallel = a.pos - c.pos
      pre_normal = fp([-parallel[1], parallel[0]])
      pre_normal_length = n.linalg.norm(pre_normal)
      if pre_normal_length != 0:
        normal = pre_normal / pre_normal_length
        b.accel += normal * force_time / b.mass * dt
      else:
        raise Exception("zero length surface segment")

  def _redistribute_surface(s):
    s._redistrubte_surface_remove()
    s._redistrubte_surface_add()

  def _redistrubte_surface_add(s):
    insertions = []

    for (a, b) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1]):
      d = n.linalg.norm(a.pos - b.pos)
      if d > s.dot_spacing:
        c = (a.pos + b.pos) / 2
        new_node = s.physenv.make_node(s.node_proto_mass, c)
        insertions.append((a, new_node))

    for (adjacent_node, new_node) in insertions:
      i = (s.nodes.index(adjacent_node) + 1) % len(s.nodes)
      s.nodes.insert(i, new_node)

  def _redistrubte_surface_remove(s):
    removals = []

    for (a, b) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1]):
      d = n.linalg.norm(a.pos - b.pos)
      if d < s.dot_spacing * 0.5:
        s.nodes.remove(a)
        s.physenv.remove_node(a)

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
      s.nodes.append(s.physenv.make_node(s.node_proto_mass, pos))

    # ## generate surface
    # s.surface = [s.physenv.make_spring(a, b, True, 100, 0.5)
    #   for (a,b) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1])]

    s.physenv.add_update_object(s)
