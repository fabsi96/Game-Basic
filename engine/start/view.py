# coding: utf-8

import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QWheelEvent
from glm.gtc.matrix_transform import *

from libs.OpenGL.DAL.Outer import *

from engine.start.control import StartControl
from libs.OpenGL.DAL.Outer.vlightsource import VLightSource
from libs.OpenGL.DAL.Outer.vmap import VMap
from libs.OpenGL.DAL.Outer.vobject import VObject
from libs.OpenGL.camera import Camera
from libs.library import Library


class StartView:
   MOUSE_SPEED = 0.5
   MIN_PITCH = 90
   MAX_PITCH = 180
   MIN_YAW = -170
   MAX_YAW = +170
   def __init__(self):
      try:
         self.models = []

         self.controller = StartControl()

         self.controller.setKeyPressCallback(self.keyPressCallback)
         self.controller.setKeyReleaseCallback(self.keyReleaseCallback)
         self.controller.setMousePressCallback(self.mousePressCallback)
         self.controller.setMouseReleaseCallback(self.mouseReleaseCallback)
         self.controller.setMouseMoveCallback(self.mouseMoveCallback)
         self.controller.setMouseWheelCallback(self.mouseWheelCallback)

         """ Light cube    
         """
         self.cube = self.controller.getLightSource()
         self.cube: VLightSource
         self.controller.addVObject(self.cube)
         self.models.append(self.cube)
         self.cube.setScale(tvec3([0.1, 0.1, 0.1]))
         self.cube.setPosition(tvec3([2.5, 0.5, 2.5]))

         """ Wall mid """
         self.wallLeft = self.controller.getVObject("testQuad")
         self.wallLeft: VObject
         self.controller.addVObject(self.wallLeft)
         self.models.append(self.wallLeft)
         currX = self.wallLeft.getPosition().x
         currY = self.wallLeft.getPosition().y
         currZ = self.wallLeft.getPosition().z
         self.wallLeft.setPosition(tvec3([currX + 2.5, currY + 2.5, currZ]))
         self.wallLeft.setScale(tvec3([2.5, 2.5, 2.5]))

         """ Wall right """
         self.wallRight = self.controller.getVObject("testQuad")
         self.wallRight: VObject
         self.controller.addVObject(self.wallRight)
         self.models.append(self.wallRight)
         currX = self.wallRight.getPosition().x
         currY = self.wallRight.getPosition().y
         currZ = self.wallRight.getPosition().z
         self.wallRight.setPosition(tvec3([currX + 5, currY + 2.5, currZ + 2.5]))
         self.wallRight.setYRotation(270)
         self.wallRight.setScale(tvec3(2.5, 2.5, 2.5))

         """ Wall left """
         self.wallMid = self.controller.getVObject("testQuad")
         self.wallMid: VObject
         self.controller.addVObject(self.wallMid)
         self.models.append(self.wallMid)
         currX = self.wallMid.getPosition().x
         currY = self.wallMid.getPosition().y
         currZ = self.wallMid.getPosition().z
         self.wallMid.setPosition(tvec3([currX, currY + 2.5, currZ + 2.5]))
         self.wallMid.setYRotation(90)
         self.wallMid.setScale(tvec3(2.5, 2.5, 2.5))

         """ Dae-Model """
         self.modelObject = self.controller.getDAEObject("kreuz.dae")
         self.modelObject: VObject
         self.controller.addVObject(self.modelObject)
         self.models.append(self.modelObject)
         self.modelObject.setPosition(tvec3([.5, 0.0, 0.0]))
         self._xrotDeg = 0.0
         self._yrotDeg = 0.0
         self._zrotDeg = 0.0
         # Standard rotation
         # Special, because model is saved in x-UP
         self.modelObject.setXRotation(270)
         self.modelObject.setZRotation(180)
         self.modelObject.setScale(tvec3([0.3, 0.3, 0.3]))
         Library.camera.followUnit(self.modelObject)

         """ Scale map
         self.scaleMap = self.controller.getScaleMap("ScaleMap")
         self.scaleMap: VObject
         self.controller.addVObject(self.scaleMap)
         self.scaleMap.setXRotation(90)
         self.scaleMap.setScale(tvec3(5.0, 5.0, 5.0))
         """
         """ Map """
         self.map = self.controller.getMap()
         self.controller.addVObject(self.map)

      except Exception as ex:
         print("{}".format(str(ex)))

      # Key Events

      # Mouse Events
      self.mouseLeftPressed = False
      self.lastMouseXPos = 0
      self.lastMouseYPos = 0


   def keyPressCallback(self, keyEvent: QKeyEvent):
      if self.models.__len__() > 0:
         self.modelObject: VObject
         if keyEvent.key() == Qt.Key_A:
            """ Turning object left """
            self.modelObject.setZRotation(self.modelObject.getZRotation() + 5)
            # Library.camera.strafeLeft()
         elif keyEvent.key() == Qt.Key_D:
            """ Turning object right """
            self.modelObject.setZRotation(self.modelObject.getZRotation() - 5)
            # Library.camera.strafeRight()
         elif keyEvent.key() == Qt.Key_W:
            """ Moving object forward """
            tPos = self.modelObject.getPosition()
            newXPos = tPos.x + sin(radians(self.modelObject.getZRotation())) * VObject.MOVEMENT_SPEED
            newZPos = tPos.z + cos(radians(self.modelObject.getZRotation())) * VObject.MOVEMENT_SPEED
            self.modelObject.setPosition(tvec3([newXPos, tPos.y, newZPos]))
            # Library.camera.moveForward()
         elif keyEvent.key() == Qt.Key_S:
            """ Moving object backward """
            tPos = self.modelObject.getPosition()
            newXPos = tPos.x - sin(radians(self.modelObject.getZRotation())) * VObject.MOVEMENT_SPEED
            newZPos = tPos.z - cos(radians(self.modelObject.getZRotation())) * VObject.MOVEMENT_SPEED
            self.modelObject.setPosition(tvec3([newXPos, tPos.y, newZPos]))
            # Library.camera.moveBackward()
         elif keyEvent.key() == Qt.Key_R:
            Library.camera._pitch = 0.0
            Library.camera._yaw = 0.0
            # Library.camera.moveUp()
         elif keyEvent.key() == Qt.Key_F:
            pass
            # Library.camera.moveDown()
         elif keyEvent.key() == Qt.Key_Escape:
            pass
         elif keyEvent.key() == Qt.Key_X:
            pass
         elif keyEvent.key() == Qt.Key_Y:
            pass
         elif keyEvent.key() == Qt.Key_Z:
            pass
         else:
            print("Key not found :: {}".format(str(keyEvent.key())))

   def keyReleaseCallback(self, keyEvent: QKeyEvent):
      pass

   def mousePressCallback(self, mouseEvent: QMouseEvent):
      if mouseEvent.button() == Qt.LeftButton:
         self.mouseLeftPressed = True

   def mouseReleaseCallback(self, mouseEvent: QMouseEvent):
      if mouseEvent.button() == Qt.LeftButton:
         self.mouseLeftPressed = False

   def mouseMoveCallback(self, mouseEvent: QMouseEvent):
      deltaX = mouseEvent.x() - self.lastMouseXPos
      deltaY = mouseEvent.y() - self.lastMouseYPos
      deltaVector = tvec2(deltaX, deltaY)
      if self.mouseLeftPressed:
         deltaLength = compute_length(deltaVector)
         self.lastMouseXPos = mouseEvent.x()
         self.lastMouseYPos = mouseEvent.y()
         if deltaLength > 50:
            return

         # Vertical (90-270)
         newPitch = Library.camera.getPitch()
         newPitch -= self.MOUSE_SPEED * deltaY
         if newPitch >= StartView.MAX_PITCH:
            newPitch = StartView.MAX_PITCH
         elif newPitch <= StartView.MIN_PITCH:
            newPitch = StartView.MIN_PITCH
         else:
            pass
         Library.camera.setPitch(newPitch)

         # Horizontal (-170 - + 170)
         newYaw = Library.camera.getYaw()
         newYaw += -self.MOUSE_SPEED * deltaX
         Library.camera.setYaw(newYaw)
         if newYaw >= StartView.MAX_YAW:
            newYaw = StartView.MAX_YAW
         elif newYaw <= StartView.MIN_YAW:
            newYaw = StartView.MIN_YAW
         else:
            pass
         Library.camera.setYaw(newYaw)

         self.lastMouseXPos = mouseEvent.x()
         self.lastMouseYPos = mouseEvent.y()

   def mouseWheelCallback(self, wheelEvent: QWheelEvent):
      try:
         if wheelEvent.angleDelta().y() > 0:
            Camera.DISTANCE_TO_TARGET -= 0.8
         else:
            Camera.DISTANCE_TO_TARGET += 0.8
      except Exception as ex:
         print(str(ex))

def main():
   try:
      myStartView = StartView()
   except Exception as ex:
      print("Exception :: {}".format(str(ex)))

if __name__ == "__main__":
   main()