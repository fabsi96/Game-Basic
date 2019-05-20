# encoding: utf-8

# System
import sys
import os
from glm.gtc.matrix_transform import *

# Libraries
from libs.OpenGL.DAL.Outer.vlightsource import VLightSource
from libs.OpenGL.DAL.Outer.vmap import VMap
from libs.OpenGL.DAL.Outer.vobject import VObject
from libs.OpenGL.Shader.NormalsShader.normalsshader import NormalsShader
from libs.OpenGL.Shader.mapShader.mapshader import MapShader
from libs.OpenGL.Shader.modelShader.modelshader import ModelShader
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

      self.__modelShader = ModelShader()
      self.__normalsShader = NormalsShader()

   # TODO
   def getLightSource(self):
      daeRawObject = RawObject()
      daeRawObject.loadDAE("testQuad.dae")
      return VLightSource(daeRawObject, self.__modelShader)

   def getMap(self):
      rawMap = RawObject()
      rawMap.loadMap2()
      return VMap(rawMap, MapShader())

   def getScaleMap(self, name: str):
      try:
         scaleMapObject = RawObject()
         scaleMapObject.loadScaleMap(name)
      except Exception as ex:
         raise ex
      return VObject(scaleMapObject, self.__modelShader, self.__normalsShader)

   def getDAEObject(self, filename:str):
      try:
         daeRawObject = RawObject()
         daeRawObject.loadDAE(filename)
      except Exception as ex:
         raise ex

      return VObject(daeRawObject, self.__modelShader, self.__normalsShader)

   def getVObject(self, name: str):
      rawObject = self.__dataController_o.getRawData(name)
      if rawObject:
         # Convert to OpenGL drawable VOpenGL
         shaderName = rawObject.shaderName

         # return this
         return VObject(rawObject, self.__modelShader, self.__normalsShader)
      else:
         return None
