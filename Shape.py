__author__ = 'ggirardin'
import random, math
from Vector import *

class Point():
  def __init__ (self, x, y):
    self.x = x
    self.y = y

  def distance (self, p): # p is another Point
     return math.sqrt ((self.x - p.x) ** 2 + (self.y - p.y) ** 2)

  def move (self, v): # v is a Vector PI/2 is up (-y)
    self.x += v.magnitude * math.cos (v.direction)
    self.y -= v.magnitude * math.sin (v.direction)

  def translate (self, xpos, ypos, theta):
    xr = self.x * math.cos (theta) - self.y * math.sin (theta) + xpos
    yr = self.y * math.cos (theta) + self.x * math.sin (theta) + ypos
    return Point (xr, yr)

class Line ():
  # a line is two verticies and a color
  def __init__ (self, p1, p2, color = None):
    self.p1 = p1
    self.p2 = p2
    self.color = color

  def translate (self, xpos, ypos, theta):
    p1r = self.p1.translate (xpos, ypos, theta)
    p2r = self.p2.translate (xpos, ypos, theta)
    return Line (p1r, p2r, self.color)

class Shape ():
  # a shape is a list of lines, x,y position, and a rotational angle
  def __init__ (self, s, p, a = 0):
    # create a shape from a list of coordinates
    # each pair of coords forms a vertex
    # each pair of vertices forms a line
    # worry about color later
    self.lines = []
    self.angle = a
    self.p = p # position is a Point

    for (x1, y1, x2, y2, c) in s:
      v1 = Point (x1, y1)
      v2 = Point (x2, y2)
      l = Line (v1, v2, c)
      self.lines.append (l)

  def translate (self):
    # make a list of translated Lines
    tlines = []

    for line in self.lines:
      tlines.append (line.translate (self.p.x, self.p.y, self.angle))
    return tlines

  def draw (self, canvas):
    tlines = self.translate ()

    for tline in tlines:
      canvas.create_line (tline.p1.x, tline.p1.y,tline.p2.x, tline.p2.y)

  def offScreen (self):
    if self.p.x < 0 or self.p.x > SCREEN_WIDTH + 10 or \
       self.p.y < 0 or self.p.y > SCREEN_HEIGHT + 10:
      return True
    else:
      return False

  def move (self, v): # v is a vector
    self.p.x += v.magnitude * math.cos (v.direction)
    self.p.y -= v.magnitude * math.sin (v.direction)