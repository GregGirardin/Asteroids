'''
A base class to handle piloting ships / AI stuff.

hList is a list of heuristics
Initially we choose the first element.


Identifier # a string to ID
Next ID
  Type (Goto, Delay, Attack)
    Goto
      Point
      ApproachType (Slow, fast)
        Slow # Try to stop at point
        Fast # Just blow past point.

    Delay
      duration
      Next

    Attack
      duration
'''
import time, math, random
from Constants import *
from Shape import *
from Ship import *
from Vector import *

class HeuristicGoto ():
  def __init__ (self, target, at):
    self.target = target
    self.approachType = at

class HeuristicWait ():
  def __init__ (self, target, duration):
    self.target = target # point to wait at
    self.duration = duration

class HeuristicAttack ():
  def __init__ (self, target, at):
    self.target = target # point to wait at



class Heuristic ():
  def __init__ (self, ident, type, next, heuristic):
    self.ident = ident
    self.type = type
    self.next = next
    self.heuristic = heuristic

# auto piloted ships inherit from this class
# they are also 'WorldObject's
class Pilot ():
  def __init__ (self, hList):
    self.hList = hList
    self.currentStateCount = 0

    if self.hList:
      self.currentH = hList [0]
    else:
      self.currentH = None

  def setHlist (self, hList):
    self.hList = hList
    self.currentH = hList [0]

  def handleGoto (self, e):
    target = self.currentH.heuristic.target # target point
    distToTarget = self.p.distanceTo (target)
    # dirToTarget = self.p.directionTo ()


  def handleWait (self, e):
    pass
  def handleAttack (self, e):
    pass

  def pilot (self, e):
    '''
    adjust, thrust, direction, and cannon based on heuristics.
    '''
    if self.hList == None or self.currentH == None:
      return
    self.currentStateCount += 1

    if self.currentH.type == HEUR_GOTO:
      self.handleGoto (e)
    elif self.currentH.type == HEUR_WAIT:
      self.handleWait (e)
    elif self.currentH.type == HEUR_ATTACK:
      self.handleAttack (e)


'''

  def pilotx (self):
    # change spin and thrust based on goal

    if self.step == GOTO_RENDESVOUS:
      # face towards it
      if self.velocity.direction < PI * .9:
        self.spin = .1
      elif self.velocity.direction > PI * 1.1:
        self.spin = -.1
      else:
        self.spin = 0

      # accelerate towards it.
      if self.velocity.magnitude < 1:
        self.thrust = .1
      else:
        self.thrust = 0

      # next step?
      if self.shape.p.x < self.rendevous:
        self.step = STOP_AT_RENDESVOUS

    elif self.step == STOP_AT_RENDESVOUS:
      if self.velocity.magnitude > .1:
        # need to stop
        self.thrust = 0
        self.spin = 0
        if self.shape.angle > PI and self.shape < TAU * .9:
          self.spin = .05
        elif self.shape.angle > PI * .1:
          self.spin = -.05
        elif self.velocity.magnitude < .2:
          self.step = WAIT_AT_RENDESVOUS
          self.waitTime = 200 + random.random() * 200
        else:
          self.thrust = .01
    elif self.step == WAIT_AT_RENDESVOUS:
      self.waitTime -= 1
      if self.rendesvousComplete or self.waitTime < 0:
        self.step = DEPART_RENDESVOUS
    elif self.step == DEPART_RENDESVOUS:
      self.thrust = 0
      self.spin = 0
      if self.shape.angle > PI and self.shape < TAU * .9:
        self.spin = .05
      elif self.shape.angle > PI * .1:
        self.spin = -.05
      elif self.velocity.magnitude < 2:
        self.thrust = .02
'''