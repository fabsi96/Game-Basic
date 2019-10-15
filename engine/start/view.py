# coding: utf-8

import sys
import os
import copy

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
   MOUSE_SPEED = 1.0
   MIN_PITCH = 90
   MAX_PITCH = 270
   MIN_YAW = -170
   MAX_YAW = +170
   """
      1) Create VObject and do settings on it
      2) Set it into map (with collision system) and /- or to 'master'-renderer (vglwindow)
      3) optional: keep track of it and use it in user-interaction (3rd player view)
   """
   # ------------------
   def __init__(self):
   # ------------------
      try:
         self.models = []

         # Inits#
         self.controller = StartControl()

         self.controller.setKeyPressCallback(self.keyPressCallback)
         self.controller.setKeyReleaseCallback(self.keyReleaseCallback)
         self.controller.setMousePressCallback(self.mousePressCallback)
         self.controller.setMouseReleaseCallback(self.mouseReleaseCallback)
         self.controller.setMouseMoveCallback(self.mouseMoveCallback)
         self.controller.setMouseWheelCallback(self.mouseWheelCallback)

         # 1#
         """ Map """
         self.map = self.controller.getMap()
         self.map: VMap

         # Lights
         # 2.1#
         self.lightSource = self.controller.getLightSource()
         self.lightSource: VObject
         self.lightSource.setPosition(tvec3(2.0, self.map.getHeight(2.0, 2.0) + 0.5, 2.0))
         self.lightSource.setScale(tvec3(0.1, 0.1, 0.1))
         self.controller.addVObject(self.lightSource)

         # 2.2#
         self.ls1: VLightSource = self.controller.getLightSource()
         self.ls1.setPosition(tvec3(13.18, self.map.getHeight(13.18, 15.00) + 0.5, 15.00))
         self.ls1.setScale(tvec3(0.1, 0.1, 0.1))
         self.controller.addVObject(self.ls1)

         # 2.3#
         self.ls2: VLightSource = self.controller.getLightSource()
         self.ls2.setPosition(tvec3(11.40, self.map.getHeight(11.40, 4.31) + 0.5, 4.31))
         self.ls2.setScale(tvec3(0.1, 0.1, 0.1))
         self.controller.addVObject(self.ls2)
         
         # 2.4#
         self.ls3: VLightSource = self.controller.getLightSource()
         self.ls3.setPosition(tvec3(14.69, self.map.getHeight(14.69, 6.44) + 0.5, 6.44))
         self.ls3.setScale(tvec3(0.1, 0.1, 0.1))
         self.controller.addVObject(self.ls3)

         # 3#
         """ Duplicate model """
         self.personModel: VObject = self.controller.getDAEObject("model.dae")
         self.personModel.setPosition(tvec3(2.5, 0.0, 2.5))
         self.personModel.setScale(tvec3(0.05, 0.05, 0.05))
         self.personModel.setXRotation(270)
         self.personModel.setZRotation(270)
         self.map.addObject(self.personModel)

         # 4#
         Library.vMap = self.map
         Library.camera.followUnit(self.personModel)

      except Exception as ex:
         print("{}".format(str(ex)))

      # Key Events

      # Mouse Events
      self.mouseLeftPressed = False
      self.lastMouseXPos = 0
      self.lastMouseYPos = 0


   def keyPressCallback(self, keyEvent: QKeyEvent):
      if keyEvent.key() == Qt.Key_A:
         """ Turning object left """

         self.personModel.setZRotation(self.personModel.getZRotation() + 5)
         """
         Library.camera.strafeLeft()
         """
      elif keyEvent.key() == Qt.Key_D:
         """ Turning object right """

         self.personModel.setZRotation(self.personModel.getZRotation() - 5)
         """
         Library.camera.strafeRight()
         """
      elif keyEvent.key() == Qt.Key_W:
         """ Moving object forward """

         tPos = self.personModel.getPosition()
         newXPos = tPos.x + sin(radians(self.personModel.getZRotation())) * VObject.MOVEMENT_SPEED
         newZPos = tPos.z + cos(radians(self.personModel.getZRotation())) * VObject.MOVEMENT_SPEED
         self.personModel.setPosition(tvec3([newXPos, tPos.y, newZPos]))
         """
         Library.camera.moveForward()
         """
      elif keyEvent.key() == Qt.Key_S:
         """ Moving object backward """

         tPos = self.personModel.getPosition()
         newXPos = tPos.x - sin(radians(self.personModel.getZRotation())) * VObject.MOVEMENT_SPEED
         newZPos = tPos.z - cos(radians(self.personModel.getZRotation())) * VObject.MOVEMENT_SPEED
         self.personModel.setPosition(tvec3([newXPos, tPos.y, newZPos]))
         """
         Library.camera.moveBackward()
         """
      elif keyEvent.key() == Qt.Key_R:
         pass
         """
         Library.camera._pitch = 0.0
         Library.camera._yaw = 0.0
         Library.camera.moveUp()
         """
      elif keyEvent.key() == Qt.Key_F:
         pass
         """
         Library.camera.moveDown()
         """
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
         """ Free camera - turning around 
         deltaLength = compute_length(deltaVector)
         self.lastMouseXPos = mouseEvent.x()
         self.lastMouseYPos = mouseEvent.y()
         if deltaLength > 50:
            return
         viewDirection = Library.camera.getViewDirection()
         toRotateAround = cross(viewDirection, Library.camera.getUpVector())
         rotator = rotate(tmat4x4([]), deltaX * -self.MOUSE_SPEED, Library.camera.getUpVector()) * \
                   rotate(tmat4x4([]), deltaY * -self.MOUSE_SPEED, toRotateAround)

         viewDirection = tmat3x3(rotator) * viewDirection
         Library.camera.setViewDirection(viewDirection)
         """

         """ Follow object calculations - Turning around object     """

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

         """ Static - must be updated every time """
         self.lastMouseXPos = mouseEvent.x()
         self.lastMouseYPos = mouseEvent.y()

   def mouseWheelCallback(self, wheelEvent: QWheelEvent):
      try:
         """ Inc/Dec distance from object """
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