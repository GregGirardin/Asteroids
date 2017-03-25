from Constants import *
from Shape import *
from Vector import *

class WorldObject ():
  # Attributes every object has.
  def __init__ (self, type, p=None, a=0.0, v=None, collisionRadius=0):
    if not v:
      v = Vector (0, 0)
    self.v = v
    self.spin = 0.0
    if not p:
      p = Point (SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2)
    self.p = p # position
    self.a = a # angle
    self.type = type
    self.accel = 0.0
    self.collisionRadius = collisionRadius

  def offScreen (self):
    if self.p.x < -SCREEN_BUFFER or self.p.x > SCREEN_WIDTH + SCREEN_BUFFER or \
       self.p.y < -SCREEN_BUFFER or self.p.y > SCREEN_HEIGHT + SCREEN_BUFFER:
      return True
    else:
      return False

  def update (self, e):
    self.a += self.spin
    if self.a < 0:
      self.a += TAU
    elif self.a > TAU:
      self.a -= TAU

    self.v.impulse (Vector (self.accel, self.a))
    self.p.move (self.v)

# Could try to make this a WorldObject if that's cleaner
class Event ():
  def __init__(self, msg, dur, action):
    self.msg = msg
    self.dur = dur
    self.action = action # callback

class gameEvents ():

  def __init__(self):
    self.eventList = []

  def newEvent (self, msg, dur, action):
    ev = Event (msg, dur, action)
    self.eventList.append (ev)

  def update (self):
    if len (self.eventList) > 0:
      e = self.eventList [0]
      e.dur -= 1
      if e.dur < 0:
        if e.action:
          e.action()
        del self.eventList [0]

    return True # Event object is always here

  def draw (self, e):
    if len (self.eventList) > 0:
      ev = self.eventList [0]
      if ev.msg:
        e.canvas.create_text (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, text = ev.msg)


# if you're facing dir and want to go goalDir, return the delta. -PI to PI
def angleTo (dir, goalDir):
  dif = goalDir - dir
  if dif > PI:
    dif -= TAU
  elif dif < -PI:
    dif += TAU

  return dif


def angleNorm (dir):
  if dir > PI:
    dir -= TAU
  elif dir < -PI:
    dir += TAU
  return dir