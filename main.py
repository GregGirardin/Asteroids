#!/usr/bin/python

from Tkinter import *
import time, math, random
from Constants import *
from Shape import *
from Ship import *
from Tanker import *
from Particles import *
from Aliens import *
from Vector import *
from Asteroid import *
from Utils import *

respawn = False

class displayEngine ():
  def __init__(self):
    self.root = Tk()
    self.canvas = Canvas (self.root, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
    self.canvas.pack()
    self.objects = []
    self.numShips = NUM_SHIPS
    self.score = 0

  def update (self):
    # collision detection (fix wasteful checks)
    for obj1 in self.objects:
      for obj2 in self.objects:
        if obj2 is not obj1:
          if obj1.type != OBJECT_TYPE_NONE and obj2.type != OBJECT_TYPE_NONE:
            rad = obj1.collisionRadius + obj2.collisionRadius
            if obj1.p.distanceTo (obj2.p) < rad:
              obj1.collision = obj2.type
              obj2.collision = obj1.type

    # update objects
    for obj in self.objects:
      if obj.update (self) == False:
        self.objects.remove (obj)

  def addObj (self, obj):
    self.objects.append (obj)

  def draw (self, ship):
    self.canvas.delete (ALL)
    for obj in self.objects:
      obj.draw (self.canvas, obj.p, obj.a)

    # game status
    # display the remaining ships
    for s in range (0, self.numShips):
       self.canvas.create_line (10 + 20 * s, 20, 15 + 20 * s,  5)
       self.canvas.create_line (15 + 20 * s,  5, 20 + 20 * s, 20)

    score = "%08s" % (self.score)
    self.canvas.create_text (100, 10, text = score)
    self.canvas.create_rectangle (200, 5, 200 + 200, 7)
    self.canvas.create_rectangle (200, 10, 200 + 200 * ship.fuel / 100, 15)
    self.canvas.create_rectangle (200, 20, 200 + 200 * ship.rounds / 100, 15)

    self.root.update()


def leftHandler (event):
  if s.spin < 0:
    s.spin = 0
  elif s.spin < MAX_SPIN:
    s.spin += SPIN_DELTA

def rightHandler (event):
  if s.spin > 0:
    s.spin = 0
  elif s.spin > -MAX_SPIN:
    s.spin -= SPIN_DELTA

def upHandler (event):
  s.accel += .01

def downHandler (event):
  s.accel = 0
  s.v.magnitude *= .8

def keyHandler (event):
  global respawn

  if event.char == " ":
    if s.collision > 0:
      respawn = True
    else:
      s.cannon = s.numRoundsPF
      if e.score:
        e.score -= 1

e = displayEngine()
s = Ship()
e.addObj (s)

e.root.bind ("<Left>",  leftHandler)
e.root.bind ("<Right>", rightHandler)
e.root.bind ("<Up>",    upHandler)
e.root.bind ("<Down>",  downHandler)
e.root.bind ("<Key>",   keyHandler)

nextAlien = 0
nextAsteroid = 0
nextTanker = 100

while True:
  e.update ()
  e.draw (s)
  time.sleep (.02)

  nextTanker -= 1
  if nextTanker < 0:
    t = Tanker()
    e.addObj(t)
    nextTanker = 1000 + random.random() * 500

  nextAsteroid -= 1
  if nextAsteroid < 0:
    a = Asteroid (20 + random.random() * 10)
    e.addObj (a)
    nextAsteroid = 200 + random.random() * 100

  nextAlien -= 1
  if nextAlien < 0:
    nextAlien = 200 + random.random() * 200
    if random.random() < .25:
      a = SmallAlien()
    else:
      a = BigAlien()
    e.addObj (a)
  if respawn:
    respawn = False
    s = Ship ()
    e.addObj (s)

e.root.mainloop()
