# encodig: utf-8

# System

# Libraries
from libs.library import Library

# DAL
from libs.OpenGL.DAL.Outer.vmap import VMap
from libs.OpenGL.DAL.Outer.vobject import VObject

# Local
from engine.control import VControl


class StartControl(VControl):
   TEST = "test"
   def __init__(self):
      super(StartControl, self).__init__()

   def getVObject(self, name:str):
      return Library.loader.getVObject(name)

   def addVObject(self, vobject: VObject):
      try:
         Library.mainWindow.glWindow.addVObject(vobject)
      except Exception as ex:
         raise ex

   def getDAEObject(self, name: str):
      return Library.loader.getDAEObject(name)

   def getScaleMap(self, name: str):
      return Library.loader.getScaleMap(name)

   def getMap(self):
      return Library.loader.getMap()

   def getLightSource(self):
      return Library.loader.getLightSource()

   def setKeyPressCallback(self, callbackFunc):
      Library.mainWindow.setKeyPressCallback(callbackFunc)

   def setKeyReleaseCallback(self, callbackFunc):
      Library.mainWindow.setKeyReleaseCallback(callbackFunc)

   def setMousePressCallback(self, callbackFunc):
      Library.mainWindow.setMousePressCallback(callbackFunc)

   def setMouseReleaseCallback(self, callbackFunc):
      Library.mainWindow.setMouseReleaseCallback(callbackFunc)

   def setMouseMoveCallback(self, callbackFunc):
      Library.mainWindow.setMouseMoveCallback(callbackFunc)

   def setMouseWheelCallback(self, callbackFunc):
      Library.mainWindow.setMouseWheelCallback(callbackFunc)