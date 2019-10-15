# encoding: utf-8

# System
import sys
import string
import re

# Libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *

from OpenGL.GL import *
from glm.gtc.matrix_transform import *

# DAL Inner
from libs.OpenGL.DAL.Inner.rawobject import *

# DAL Outer
from libs.OpenGL.DAL.Outer import *
from libs.OpenGL.DAL.Outer.vobject import VObject
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL
from libs.OpenGL.Shader.shaderprogram import ShaderProgram

from libs.OpenGL.Shader.shaderloader import *
from libs.library import Library


class VWindow(QWidget):
   def __init__(self,locX, locY, width, height, parent=None):
      super(VWindow, self).__init__(parent)
      self.glWindow = VGLWindow(self)
      self.qTimer = None

      self.setWindowTitle("OpenGL Window")
      self.setGeometry(locX, locY, width, height)

      self.createIntervallTimer(1)

      self.keyPressCallbackFunc = None
      self.keyReleaseCallbackFunc = None
      self.mousePressCallbackFunc = None
      self.mouseReleaseCallbackFunc = None
      self.mouseMoveCallbackFunc = None
      self.mouseWheelCallbackFunc = None

      self._projectionMatrix = None

   def getProjectionMatrix(self):
      self._projectionMatrix = perspective(120.0, self.width() / self.height(), 0.1, 1000.0)
      return self._projectionMatrix

   def setKeyPressCallback(self, callbackFunc):
      self.keyPressCallbackFunc = callbackFunc

   def setKeyReleaseCallback(self, callbackFunc):
      self.keyReleaseCallbackFunc = callbackFunc

   def setMousePressCallback(self, callbackFunc):
      self.mousePressCallbackFunc = callbackFunc

   def setMouseReleaseCallback(self, callbackFunc):
      self.mouseReleaseCallbackFunc = callbackFunc

   def setMouseMoveCallback(self, callbackFunc):
      self.mouseMoveCallbackFunc = callbackFunc

   def setMouseWheelCallback(self, callbackFunc):
      self.mouseWheelCallbackFunc = callbackFunc

   def createIntervallTimer(self, milliSeconds):
      self.qTimer = QTimer(self)
      self.qTimer.setInterval(milliSeconds)
      self.qTimer.timeout.connect(self.glWindow.update)
      self.qTimer.start()

   def keyPressEvent(self, keyEvent: QKeyEvent):
      if self.keyPressCallbackFunc:
         self.keyPressCallbackFunc(keyEvent)
      self.glWindow.update()

   def keyReleaseEvent(self, keyEvent: QKeyEvent):
      if self.keyReleaseCallbackFunc:
         self.keyReleaseCallbackFunc(keyEvent)
      self.glWindow.update()

   def mousePressEvent(self, mouseEvent: QMouseEvent):
      if self.mousePressCallbackFunc:
         self.mousePressCallbackFunc(mouseEvent)
      self.glWindow.update()

   def mouseMoveEvent(self, mouseEvent: QMouseEvent):
      if self.mouseMoveCallbackFunc:
         self.mouseMoveCallbackFunc(mouseEvent)
      self.glWindow.update()

   def mouseReleaseEvent(self, mouseEvent: QMouseEvent):
      if self.mouseReleaseCallbackFunc:
         self.mouseReleaseCallbackFunc(mouseEvent)
      self.glWindow.update()

   def wheelEvent(self, wheelEvent: QWheelEvent):
      if self.mouseWheelCallbackFunc:
         self.mouseWheelCallbackFunc(wheelEvent)
      self.glWindow.update()

   def resizeEvent(self, qResize):
      windowSize = self.frameGeometry()
      self.glWindow.setGeometry(0, 0, windowSize.width(), windowSize.height())
      self.glWindow.update()

   def close(self):
      # self.qTimer.stop()
      pass

class VGLWindow(QGLWidget):
   ShaderVersion = 440
   def __init__(self, parent):
      QGLWidget.__init__(self, parent)
      parentSize = self.parent().frameGeometry()
      self.setGeometry(parentSize)
      self.objects = []

   def addVObject(self, obj: VOpenGL):
      self.objects.append(obj)

   def initializeGL(self):
      try:
         glClearColor(0.0, 0.0, 0.0, 1.0)
         glEnable(GL_DEPTH_TEST)
         glEnable(GL_TEXTURE_2D)
         # CLOCKWISE
         glEnable(GL_CULL_FACE)
         glEnable(GL_TEXTURE_CUBE_MAP)
         QApplication.setKeyboardInputInterval(1)
         print("OpenGL INFO :: \n {0}".format(VGLWindow.getOpenglInfo()))

      except Exception as ex:
         print("initializeGL() - Exception :: {0}".format(str(ex)))

   def paintGL(self):
      try:
         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

         Library.camera.update()
         for obj in self.objects:
            obj.render()
         if Library.vMap is not None:
            Library.vMap.render()
         """
         for obj in self.objects:
            obj.renderNormalsVertices()
         """
      except Exception as ex:
         print("paintGL() - Exception :: {0}".format(str(ex)))

   def resizeGL(self, width, height):
      glViewport(0, 0, width, height)

   @staticmethod
   def getOpenglInfo():

      info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
        """.format(
         glGetString(GL_VENDOR),
         glGetString(GL_RENDERER),
         glGetString(GL_VERSION),
         glGetString(GL_SHADING_LANGUAGE_VERSION))
      versionStr : str = glGetString(GL_SHADING_LANGUAGE_VERSION).decode('ascii')
      versionStr = re.sub("\D", "", versionStr) # \D -> (D)igits
      print("Version string :: {}".format(versionStr))
      VGLWindow.ShaderVersion = int(versionStr)
      return info

