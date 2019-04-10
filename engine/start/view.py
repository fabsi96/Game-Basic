# coding: utf-8

import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from glm.gtc.matrix_transform import *

from libs.OpenGL.DAL.Outer import *

from engine.start.control import StartControl
from libs.OpenGL.DAL.Outer.vobject import VObject
from libs.library import Library


class StartView:
   MOUSE_SPEED = 0.01
   def __init__(self):
      try:
         self.models = []

         self.controller = StartControl()

         self.controller.setKeyPressCallback(self.keyPressCallback)
         self.controller.setKeyReleaseCallback(self.keyReleaseCallback)
         self.controller.setMousePressCallback(self.mousePressCallback)
         self.controller.setMouseReleaseCallback(self.mouseReleaseCallback)
         self.controller.setMouseMoveCallback(self.mouseMoveCallback)

         """ Light cube 
         self.cube = self.controller.getVObject("testCube")
         self.cube: VObject
         self.controller.addVObject(self.cube)
         self.models.append(self.cube)
         self.cube.setScale(0.1, 0.1, 0.1)
         self.cube.setPosition(2, 1.8, 1.7)
         """


         """ Wall left """
         self.wallLeft = self.controller.getVObject("testQuad")
         self.wallLeft: VObject
         self.controller.addVObject(self.wallLeft)
         self.models.append(self.wallLeft)
         currX = self.wallLeft.getPosition().x
         currY = self.wallLeft.getPosition().y
         currZ = self.wallLeft.getPosition().z

         self.wallLeft.setPosition(currX + 2.5, currY + 2.5, currZ)
         self.wallLeft.setScale(2.5, 2.5, 2.5)

         """ Wall right """
         self.wallRight = self.controller.getVObject("testQuad")
         self.wallRight: VObject
         self.controller.addVObject(self.wallRight)
         self.models.append(self.wallRight)
         currX = self.wallRight.getPosition().x
         currY = self.wallRight.getPosition().y
         currZ = self.wallRight.getPosition().z

         self.wallRight.setPosition(currX + 5, currY + 2.5, currZ + 2.5)
         self.wallRight.setRotation(0, 1, 0, 270)

         self.wallRight.setScale(2.5, 2.5, 2.5)

         self.modelObject = self.controller.getDAEObject("model.dae")
         self.modelObject: VObject
         self.controller.addVObject(self.modelObject)
         self.models.append(self.modelObject)
         self.modelObject.setPosition(2, 0.0, 1.0)
         self.modelObject.setRotation(1, 0, 0, 270)
         self.modelObject.setScale(0.3, 0.3, 0.3)

         """ Map"""
         self.map = self.controller.getScaleMap("ScaleMap")
         self.map: VObject
         self.controller.addVObject(self.map)
         self.map.setRotation(1, 0, 0, 90)
         self.map.setScale(5, 5, 5)
      except Exception as ex:
         print("{}".format(str(ex)))
      # Key Events

      # Mouse Events
      self.mouseLeftPressed = False
      self.lastMouseXPos = 0
      self.lastMouseYPos = 0


   def keyPressCallback(self, keyEvent: QKeyEvent):
      if self.models.__len__() > 0:
         if keyEvent.key() == Qt.Key_A:
            Library.camera.strafeLeft()
         elif keyEvent.key() == Qt.Key_D:
            Library.camera.strafeRight()
         elif keyEvent.key() == Qt.Key_W:
            Library.camera.moveForward()
         elif keyEvent.key() == Qt.Key_S:
            Library.camera.moveBackward()
         elif keyEvent.key() == Qt.Key_R:
            Library.camera.moveUp()
         elif keyEvent.key() == Qt.Key_F:
            Library.camera.moveDown()
         elif keyEvent.key() == Qt.Key_Escape:
            # Library.mainWindow.close()
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
         viewDirection = Library.camera.getViewDirection()
         toRotateAround = cross(viewDirection, Library.camera.getUpVector())
         rotator = rotate(tmat4x4([]), deltaX * -self.MOUSE_SPEED, Library.camera.getUpVector()) * \
                   rotate(tmat4x4([]), deltaY * -self.MOUSE_SPEED, toRotateAround)

         viewDirection = tmat3x3(rotator) * viewDirection
         Library.camera.setViewDirection(viewDirection)

         self.lastMouseXPos = mouseEvent.x()
         self.lastMouseYPos = mouseEvent.y()

def main():
   try:
      myStartView = StartView()
   except Exception as ex:
      print("Exception :: {}".format(str(ex)))

if __name__ == "__main__":
   main()