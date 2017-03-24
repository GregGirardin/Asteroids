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

class displayEngine ():
  def __init__ (self):
    self.root = Tk()
    self.canvas = Canvas (self.root, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
    self.canvas.pack()
    self.highScore = 0
    self.newGame()

  def newGame (self):
    self.objects = []
    self.numShips = NUM_SHIPS
    self.score = 0
    self.respawn = True
    self.newWave (1)

  def newWave (self, wave):
    t = "Wave %d" % wave
    if wave > 1:
      self.canvas.create_text (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, text = t)
      self.root.update()
      time.sleep (2)

    self.remainingAsteroids = 10 * wave
    self.remainingAliens = 10 * wave
    self.wave = wave
    self.nextTanker = random.uniform (2000, 2500)
    self.nextAlien = random.uniform (100, 200)
    self.nextAsteroid = random.uniform (100, 200)

  def gameOver (self):
    if self.score > self.highScore:
      self.highScore = self.score
    self.newGame()
    s = None
    t = "You have failed fuckhead."
    self.canvas.create_text (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, text = t)
    self.root.update()

    time.sleep (5)

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

    # spawn stuff
    self.nextTanker -= 1
    if self.nextTanker < 0:
      e.addObj (Tanker())
      self.nextTanker = random.uniform (2000, 2500)

    if self.remainingAsteroids > 0:
      self.nextAsteroid -= 1
      if self.nextAsteroid < 0:
        self.remainingAsteroids -= 1
        self.nextAsteroid = random.uniform (100, 200)
        e.addObj (Asteroid (random.uniform (20, 30)))

    if self.remainingAliens > 0:
      self.nextAlien -= 1
      if self.nextAlien < 0:
        self.remainingAliens -= 1
        self.nextAlien = random.uniform (100, 200)
        if random.random() < .25:
          a = SmallAlien()
        else:
          a = BigAlien()
        e.addObj (a)

    if self.numShips < 0:
      self.gameOver()
    else:
    # check if wave complete
      if self.remainingAsteroids == 0 and self.remainingAliens == 0:
        complete = True
        for obj in self.objects:
          if obj.type == OBJECT_TYPE_ALIEN or obj.type == OBJECT_TYPE_ASTEROID:
            complete = False
            break
        if complete == True:
          self.wave += 1
          if self.wave > NUM_WAVES:
            self.gameOver()
          else:
            self.newWave (self.wave)

  def addObj (self, obj):
    self.objects.append (obj)

  def draw (self):
    self.canvas.delete (ALL)
    for obj in self.objects:
      obj.draw (self.canvas, obj.p, obj.a)

    # display the remaining ships
    for s in range (0, self.numShips):
       self.canvas.create_line (10 + 20 * s, 20, 15 + 20 * s,  5)
       self.canvas.create_line (15 + 20 * s,  5, 20 + 20 * s, 20)

    t = "Score %08s" % self.score
    self.canvas.create_text (600, 10, text = t)
    t = "High %08s" % self.highScore
    self.canvas.create_text (700, 10, text = t)
    t = "Wave %d" % self.wave
    self.canvas.create_text (350, 10, text = t)

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
  if event.char == " ":
    if s.collision > 0:
      e.respawn = True
    else:
      s.cannon = s.numRoundsPF
      if e.score:
        e.score -= 1

e = displayEngine()

e.root.bind ("<Left>",  leftHandler)
e.root.bind ("<Right>", rightHandler)
e.root.bind ("<Up>",    upHandler)
e.root.bind ("<Down>",  downHandler)
e.root.bind ("<Key>",   keyHandler)

while True:
  time.sleep (.02)

  if e.respawn == True:
    e.respawn = False
    s = Ship()
    e.addObj (s)

  e.update ()
  e.draw ()

# e.root.mainloop()
