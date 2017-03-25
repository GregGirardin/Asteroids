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

debugVectors = False

class HeuristicGoto ():
  def __init__ (self, target, distance, duration, at = APPROACH_TYPE_SLOW):
    self.target = target
    self.distance = distance # close do we need to get for success
    self.duration = duration
    self.targetReached = False
    self.approachType = at

class HeuristicWait ():
  def __init__ (self, duration):
    self.duration = duration

class HeuristicAttack ():
  def __init__ (self, duration = 50):
    self.duration = duration
    self.durationCounter = duration
    self.attackState = ATTACK_INIT
    self.aangleOffset = random.uniform (-.2, .2) # shoot a bit randomly
    self.ttNextAttack = 1
####

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

    if h.targetReached: # try to turn around and top
      if self.v.magnitude > SPEED_SLOW / 6:
        # turn around
        targetDir = angleNorm (self.v.direction + PI)
        dirTo = angleTo (self.a, targetDir)
        if math.fabs (dirTo) > .1:
          self.accel = 0
          self.spin = dirTo / 20
        else:
          self.accel = THRUST_HI
          self.spin = 0
      else:
        self.accel = 0
        self.spin = 0
        dirTo = self.v.direction
      targetVector = Vector (self.accel, dirTo)
      desiredVec = Vector (0, 0)
    else: # haven't reached the target yet
      distToTarget = self.p.distanceTo (target) # determine ideal speed based on distance
      targetSpeed = 0

      if distToTarget > OBJECT_DIST_FAR:
        targetSpeed = SPEED_HI
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
      if h.approachType == APPROACH_TYPE_FAST:
        targetSpeed = SPEED_HI

      dirToTarget = self.p.directionTo (target)
      targetVector = Vector (targetSpeed, dirToTarget) # Ideal velocity vector from 'p' to target
      correctionVec = vectorDiff (self.v, targetVector) # vector to make our velocity approach targetVector

      # If we're pretty close to targetVector, just go straight
      # Continuous adjustment causes erratic behavior.
      desiredVec = targetVector if correctionVec.magnitude < targetVector.magnitude / 3 else correctionVec

      da = angleTo (self.a, desiredVec.direction)

      self.spin = da / 20
      dp = dot (self.v, desiredVec) # component of velocity in the direction of correctionVec
      if dp < SPEED_HI:
        self.accel = THRUST_HI
      elif dp < SPEED_MED:
        self.accel = THRUST_LOW
      else:
        self.accel = 0
        self.spin = 0

    if debugVectors:
      self.tv = targetVector
      self.cv = desiredVec
      self.target = target

    if h.targetReached == True:
      h.duration -= 1
      if h.duration < 0:
        h.targetReached = False # in cause we use this one again
        return True
    return False

  def handleWait (self, e):
    h = self.currentH.heuristic
    self.accel = 0
    self.spin = 0

    h.duration -= 1
    if h.duration < 0:
      return True

    return False

  def handleAttack (self, e):
    h = self.currentH.heuristic

    h.durationCounter -= 1
    if h.durationCounter <= 0:
      h.durationCounter = h.duration
      return True

    if h.attackState == ATTACK_INIT:
      if h.ttNextAttack == 0:
        h.attackState = ATTACK_ALIGN
        h.aangleOffset = random.uniform (-.2, .2) # shoot a bit randomly
      else:
        h.ttNextAttack -= 1

    if h.attackState == ATTACK_ALIGN:
      s = None
      for obj in e.objects:
        if obj.type == OBJECT_TYPE_SHIP:
          s = obj
          break

      if not s:
        return True

      goalDir = dir (s.p.x - self.p.x, s.p.y - self.p.y) + h.aangleOffset
      aToGoal = angleTo (self.a, goalDir)

      if math.fabs (aToGoal) < .1:
        self.cannon = 1 # cannon handled in update
        h.attackState = ATTACK_INIT
        h.ttNextAttack = random.randrange (20, 70)
      else:
        self.spin = aToGoal / 10

    # are we facing sort of in the direction of the Ship

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