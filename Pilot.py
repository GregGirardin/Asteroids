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
  def __init__ (self, target, distance, duration):
    self.target = target
    self.distance = distance # close do we need to get for success
    self.duration = duration
    self.targetReached = False

class HeuristicWait ():
  def __init__ (self, target, duration):
    self.target = target # point to wait at
    self.duration = duration

class HeuristicAttack ():
  def __init__ (self, target, at):
    self.target = target # point to wait at


class Heuristic ():
  def __init__ (self, id, type, next, heuristic):
    self.id = id
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
    h = self.currentH.heuristic
    target = h.target # target point

    distToTarget = self.p.distanceTo (target) # determine ideal speed based on distance
    targetSpeed = 0
    if distToTarget > OBJECT_DIST_FAR:
      targetSpeed = SPEED_FAST
    elif distToTarget > OBJECT_DIST_MED:
      if h.distance == OBJECT_DIST_FAR:
        h.targetReached = True
      targetSpeed = SPEED_MED
    elif distToTarget > OBJECT_DIST_NEAR:
      if h.distance == OBJECT_DIST_MED:
        h.targetReached = True
      targetSpeed = SPEED_SLOW
    else:
      h.targetReached = True

    dirToTarget = self.p.directionTo (target)
    targetVector = Vector (targetSpeed, dirToTarget) # Ideal velocity vector from 'p' to target
    correctionVec = vectorDiff (self.v, targetVector) # vector to take us towards our targetVector

    da = angleTo (self.a, correctionVec.direction)
    self.spin = da / 20
    if correctionVec.magnitude > self.v.magnitude:
      self.accel = THRUST_HI
    else:
      self.accel = 0

    if h.targetReached == True:
      h.duration -= 1
      if h.duration < 0:
        return True
    return False


  def handleWait (self, e):
    h = self.currentH.heuristic

    h.duration -= 1
    if h.duration < 0:
      return True

    return False

  def handleAttack (self, e):
    return False

  def pilot (self, e):
    '''
    adjust, thrust, direction, and cannon based on heuristics.
    '''
    if self.hList == None or self.currentH == None:
      return
    self.currentStateCount += 1

    s = False

    if self.currentH.type == HEUR_GOTO:
      s = self.handleGoto (e)
    elif self.currentH.type == HEUR_WAIT:
      s = self.handleWait (e)
    elif self.currentH.type == HEUR_ATTACK:
      s = self.handleAttack (e)

    if s == True:
      for h in self.hList:
        if h.id == self.currentH.next:
          self.currentH = h
          break