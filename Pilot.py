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

class HeuristicGo ():
  def __init__(self, velocity, duration):
    self.hVelocity = velocity
    self.hDuration = duration

class HeuristicFace():
  def __init__(self, angle):
    self.hAngle = angle

class HeuristicStop():
  pass

class HeuristicGoto ():
  def __init__ (self, target, distance):
    self.target = target
    self.distance = distance # close do we need to get for success
    self.targetReached = False

def HeuristicGotoRandom():
  return (HeuristicGoto (Point (SCREEN_WIDTH  * random.random (),
                                SCREEN_HEIGHT * random.random ()),
                          OBJECT_DIST_MED))

class HeuristicWait ():
  def __init__ (self, duration):
    self.hDuration = duration

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

# Auto piloted things inherit from this class. They are also "WorldObject"s
class Pilot ():
  def __init__ (self, hList):
    self.hList = hList
    self.currentStateCount = 0

    if self.hList:
      self.currentH = hList [0]
    else:
      self.currentH = None

    if debugVectors:
      self.tv = Vector (0,0)
      self.cv = Vector (0,0)
      self.target = Point (0,0)

  def setHlist (self, hList):
    self.hList = hList
    self.currentH = hList [0]

  def handleGo (self, e):
    h = self.currentH.heuristic
    if h.hDuration > 0:
      h.hDuration -= 1
      if self.v.magnitude < h.hVelocity:
        self.accel = THRUST_MED
      else:
        self.accel = 0
      return False
    else:
      return True

  def handleFace (self, e):
    h = self.currentH.heuristic
    dirTo = angleTo (self.a, h.hAngle)
    if math.fabs (dirTo) > .05:
      self.spin = dirTo / 20
      return False
    else:
      self.spin = 0
      return True

  def handleStop (self, e):
    if self.v.magnitude > SPEED_SLOW / 20:
      # turn around
      targetDir = angleNorm (self.v.direction + PI)
      dirTo = angleTo (self.a, targetDir)
      if math.fabs (dirTo) > .05:
        self.accel = 0
        self.spin = dirTo / 20
      else:
        self.accel = THRUST_HI
        self.spin = 0
      return False

    self.accel = 0
    self.spin = 0
    return True

  def handleGoto (self, e):
    h = self.currentH.heuristic

    target = h.target # target point

    # determine ideal vector based on distance
    distToTarget = self.p.distanceTo (target)

    self.accel = 0
    self.spin = 0

    if ((distToTarget < OBJECT_DIST_FAR) and
        ((h.distance == OBJECT_DIST_FAR) or
         ((distToTarget > OBJECT_DIST_MED and h.distance == OBJECT_DIST_MED) or
         (distToTarget < OBJECT_DIST_NEAR)))):
      return True

    dirToTarget = self.p.directionTo (target)
    targetVector = Vector (SPEED_HI * 1.5, dirToTarget) # hack. Long vector and drag smooth out ship.
    correctionVec = vectorDiff (self.v, targetVector) # vector to make our velocity approach targetVector

    # If we're pretty close to targetVector, just go straight
    # Continuous adjustment causes erratic behavior.
    desiredVec = correctionVec # targetVector if correctionVec.magnitude < targetVector.magnitude / 3 else correctionVec

    da = angleTo (self.a, desiredVec.direction)

    self.spin = da / 20
    dp = dot (self.v, desiredVec) # component of velocity in the direction of correctionVec
    if dp < SPEED_HI:
      self.accel = THRUST_HI
    elif dp < SPEED_MED:
      self.accel = THRUST_LOW

    # Cheating. Drag allows us to stay behind target vector. Tricky to fix and this works.
    # otherwise you have to deal with turning around to slow down if you're too fast.
    self.v.magnitude *= .99

    if debugVectors:
      self.tv = targetVector
      self.cv = desiredVec
      self.target = target

    return False

  def handleWait (self, e):
    h = self.currentH.heuristic
    self.accel = 0
    self.spin = 0

    h.hDuration -= 1
    if h.hDuration < 0:
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
    Adjust, thrust, direction, and cannon based on heuristics.
    '''
    if self.hList == None or self.currentH == None:
      return
    self.currentStateCount += 1

    s = False

    if self.currentH.type == HEUR_GO:
      s = self.handleGo (e)
    if self.currentH.type == HEUR_FACE:
      s = self.handleFace (e)
    if self.currentH.type == HEUR_STOP:
      s = self.handleStop (e)
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