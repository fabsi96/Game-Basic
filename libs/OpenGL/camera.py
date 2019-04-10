# encoding: utf-8
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL
from glm.gtc.matrix_transform import *

class Camera:
   MOVEMENT_SPEED = 0.1
   def __init__(self):
      self._position = tvec3([0.0, 0.0, 0.0])
      self._viewDirection = tvec3([0.0, 0.0, -1.0])
      self._upVector = tvec3([0.0, 1.0, 0.0])

   def followUnit(self, target: VOpenGL):
      pass

   def getViewDirection(self):
      return self._viewDirection
   def getUpVector(self):
      return self._upVector
   def setViewDirection(self, newViewDirection: tvec3):
      self._viewDirection = newViewDirection
   def setUpVector(self, newUpVector: tvec3):
      self._upVector = newUpVector

   def getWorldToViewMatrix(self):
      return lookAt(self._position, self._position + self._viewDirection, self._upVector)

   def moveForward(self):
      self._position += Camera.MOVEMENT_SPEED * self._viewDirection
   def moveBackward(self):
      self._position += -Camera.MOVEMENT_SPEED * self._viewDirection
   def moveDown(self):
      self._position += -Camera.MOVEMENT_SPEED * self._upVector
   def moveUp(self):
      self._position += Camera.MOVEMENT_SPEED * self._upVector
   def moveRight(self):
      pass
   def moveLeft(self):
      pass
   def strafeRight(self):
      strafeDirection = cross(self._viewDirection, self._upVector)
      self._position += Camera.MOVEMENT_SPEED * strafeDirection
   def strafeLeft(self):
      strafeDirection = cross(self._viewDirection, self._upVector)
      self._position += -Camera.MOVEMENT_SPEED * strafeDirection