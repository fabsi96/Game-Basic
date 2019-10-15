# encoding: utf-8
from libs.OpenGL.DAL.Outer.vobject import VObject
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL
from glm.gtc.matrix_transform import *

class Camera:
   MOVEMENT_SPEED = 0.2
   DISTANCE_TO_TARGET = 3
   # -------------------------------
   def __init__(self, target=None):
   # -------------------------------
      self._position = tvec3([8.6, 14.25, 31.1])
      self._viewDirection = tvec3([0.01661774143576622 , -0.5563605427742004 , -0.8307739496231079])
      self._upVector = tvec3([0.0, 1.0, 0.0])

      self._targetUnit = target
      # Vertical additional
      self._pitch = 90
      # Horizontal additional
      self._yaw = 0.0

   # -------------------------------
   def followUnit(self, target: VOpenGL):
   # -------------------------------
      self._targetUnit = target

   """ Follow object calculations """
   # -------------------------------
   def update(self):
   # -------------------------------
      try:
         if self._targetUnit is not None:
            self._targetUnit: VObject
            targetYRotation = self._targetUnit.getZRotation()
            tPos = self._targetUnit.getPosition()
            newXPosition = tPos.x - Camera.DISTANCE_TO_TARGET * sin(radians(targetYRotation + self._yaw))
            newYPosition = tPos.y + Camera.DISTANCE_TO_TARGET * sin(radians(self._pitch))
            newZPosition = tPos.z - Camera.DISTANCE_TO_TARGET * cos(radians(targetYRotation + self._yaw))

            self._position = tvec3([newXPosition, newYPosition, newZPosition])
            self._viewDirection = tPos - self._position
         else:
            pass
      except Exception as ex:
         raise ex

   """ Getter """
   # -------------------------------
   def getPosition(self):
   # -------------------------------
      return self._position
   # -------------------------------
   def getViewDirection(self):
   # -------------------------------
      return self._viewDirection
   # -------------------------------
   def getUpVector(self):
   # -------------------------------
      return self._upVector

   # -------------------------------
   def setViewDirection(self, newViewDirection: tvec3):
   # -------------------------------
      self._viewDirection = newViewDirection
   # -------------------------------
   def setUpVector(self, newUpVector: tvec3):
   # -------------------------------
      self._upVector = newUpVector

   # For following objects
   # -------------------------------
   def getPitch(self):
   # -------------------------------
      return self._pitch
   # -------------------------------
   def getYaw(self):
   # -------------------------------
      return self._yaw

   # -------------------------------
   def setPitch(self, value):
   # -------------------------------
      self._pitch = value
   # -------------------------------
   def setYaw(self, value):
   # -------------------------------
      self._yaw = value

   """ View matrix for shaders """
   # -------------------------------
   def getWorldToViewMatrix(self):
   # -------------------------------
      return lookAt(self._position, self._position + self._viewDirection, self._upVector)

   """ Camera movement """
   # -------------------------------
   def moveForward(self):
   # -------------------------------
      self._position += Camera.MOVEMENT_SPEED * self._viewDirection
   # -------------------------------
   def moveBackward(self):
   # -------------------------------
      self._position += -Camera.MOVEMENT_SPEED * self._viewDirection
   # -------------------------------
   def moveDown(self):
   # -------------------------------
      self._position += -Camera.MOVEMENT_SPEED * self._upVector
   # -------------------------------
   def moveUp(self):
   # -------------------------------
      self._position += Camera.MOVEMENT_SPEED * self._upVector

   # -------------------------------
   def moveRight(self):
   # -------------------------------
      pass

   # -------------------------------
   def moveLeft(self):
   # -------------------------------
      pass

   # -------------------------------
   def strafeRight(self):
   # -------------------------------
      strafeDirection = cross(self._viewDirection, self._upVector)
      self._position += Camera.MOVEMENT_SPEED * strafeDirection
   # -------------------------------
   def strafeLeft(self):
   # -------------------------------
      strafeDirection = cross(self._viewDirection, self._upVector)
      self._position += -Camera.MOVEMENT_SPEED * strafeDirection

