# encoding: utf-8

# System
import sys
import os
from glm.gtc.matrix_transform import *

# Libraries
from libs.OpenGL.DAL.Outer.light import VLight
from libs.OpenGL.DAL.Outer.vobject import VObject
from libs.OpenGL.Shader.shaderprogram import ShaderProgram
from libs.OpenGL.Shader.shaderloader import getShader
from libs.Qt.vwindow import VGLWindow

# DAL Inner
from libs.OpenGL.DAL.Inner.rawobject import RawObject

# DAL Outer
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL

# Global
from settings import *

# Local
from libs.OpenGL.DataLoader.sqlitecontrol import DataControl


class DataLoader:
   LIBRARY = dict()

   # Database information
   DATA_PREFIX = "data"
   DATA_SUFFIX = ".sqlite"
   DATA_LOGIN = ""

   DEFAULT_SHADER_NAME = "modelShader"

   dataInformation_o = None
   dataController_o = None

   def __init__(self):
      self.__dataInformation_o = Settings.dataSettings
      fullPath_s = os.path.join(os.getcwd(), self.__dataInformation_o["path"])
      self.__dataController_o = DataControl(fullPath_s, DataLoader.DATA_PREFIX + DataLoader.DATA_SUFFIX)

      self.__defaultShader = ShaderProgram(DataLoader.DEFAULT_SHADER_NAME, getShader("libs/OpenGL/Shader/" + DataLoader.DEFAULT_SHADER_NAME, DataLoader.DEFAULT_SHADER_NAME, DataLoader.DEFAULT_SHADER_NAME, VGLWindow.ShaderVersion))

   # TODO
   def getLightSource(self, lightMode):
      if lightMode == "diffuse":
         return VLight(self.__dataController_o.getRawData("testCube"), tvec3([2, 1.8, 1.7]), self.__defaultShader)
      elif lightMode == "ambient":
         pass
      elif lightMode == "specular":
         pass
      else:
         raise Exception("Unknown lightsource")


   def getScaleMap(self, name: str):
      try:
         scaleMapObject = RawObject()
         scaleMapObject.loadScaleMap(name)
      except Exception as ex:
         raise ex
      return VObject(scaleMapObject, self.__defaultShader)

   def getDAEObject(self, filename:str):
      try:
         daeRawObject = RawObject()
         daeRawObject.loadDAE(filename)
      except Exception as ex:
         raise ex

      return VObject(daeRawObject, self.__defaultShader)

   def getVObject(self, name: str):
      rawObject = self.__dataController_o.getRawData(name)
      if rawObject:
         # Convert to OpenGL drawable VOpenGL
         shaderName = rawObject.shaderName

         # return this
         return VObject(rawObject, self.__defaultShader)
      else:
         return None
