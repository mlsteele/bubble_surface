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
    s.dot_spacing = 5.0 # mesh density
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

  def has_settled(s):
    # return abs(s.calc_area() / s.area - 1) < 0.0005 \
    # print sum(n.linalg.norm(node.vel) for node in s.nodes) / len(s.nodes)
    # print max(n.linalg.norm(node.vel) for node in s.nodes)
    return (abs(s.calc_area() / s.area - 1) < 0.0001) and all(n.linalg.norm(node.vel) < 10 for node in s.nodes)

  def print_info(s):
    print "\nbubble info\n----------"
    print "avg vel: %s" % (sum(n.linalg.norm(node.vel) for node in s.nodes) / len(s.nodes))
    print "max vel: %s" % max(n.linalg.norm(node.vel) for node in s.nodes)
    print "current area: %s" % (s.calc_area())
    print "area ratio: %s" % (s.calc_area() / s.area)
    print "area diff: %s" % (s.calc_area() - s.area)

  def update(s, dt):
    s._redistrubte_surface_add()
    s._redistrubte_surface_remove()
    s._contract(dt)
    s._expand(dt)

  def _contract(s, dt):
    # force_time = 8000.
    # for (a,b,c) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1], s.nodes[2:] + s.nodes[0:2]):
    #   d = (a.pos + c.pos - 2 * b.pos)
    #   dl = n.linalg.norm(d)
    #   if dl != 0:
    #     b.accel += d / dl * force_time / b.mass * dt
    force_time = 3000.
    for (a,b,c) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1], s.nodes[2:] + s.nodes[0:2]):
      d = (a.pos + c.pos - 2 * b.pos)
      b.accel += d * force_time / b.mass * dt

  def _expand(s, dt):
    if s.calc_area() > s.area: return

    force_time = 8000.
    for (a,b,c) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1], s.nodes[2:] + s.nodes[0:2]):
      parallel = a.pos - c.pos
      pre_normal = fp([-parallel[1], parallel[0]])
      pre_normal_length = n.linalg.norm(pre_normal)
      if pre_normal_length != 0:
        normal = pre_normal / pre_normal_length
        b.accel += normal * force_time / b.mass * dt
      else:
        raise Exception("zero length surface segment")

  def _redistrubte_surface_add(s):
    insertions = []

    for (a, b) in zip(s.nodes, s.nodes[1:] + s.nodes[0:1]):
      d = n.linalg.norm(a.pos - b.pos)
      if d > s.dot_spacing:
        if not s.physenv.test_line_against_walls(a.pos, b.pos):
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
