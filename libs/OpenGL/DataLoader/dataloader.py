# encoding: utf-8

# System
import sys
import os
from glm.gtc.matrix_transform import *

# Libraries
from libs.OpenGL.DAL.Outer.vcubemap import VCubeMap
from libs.OpenGL.DAL.Outer.vlightsource import VLightSource
from libs.OpenGL.DAL.Outer.vmap import VMap
from libs.OpenGL.DAL.Outer.vobject import VObject
from libs.OpenGL.Shader.NormalsShader.normalsshader import NormalsShader
from libs.OpenGL.Shader.cubeMapShader.cubeMapShader import CubeMapShader
from libs.OpenGL.Shader.mapShader.mapshader import MapShader
from libs.OpenGL.Shader.modelShader.modelshader import ModelShader

# DAL Inner
from libs.OpenGL.DAL.Inner.rawobject import RawObject

# DAL Outer

# Global
from libs.library import Library
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


      self.__skyBox = self.getSkyBox()

      Library.mainWindow.glWindow.addVObject(self.__skyBox)

   def getVObject(self, name: str):
      rawObject = self.__dataController_o.getRawData(name)
      if rawObject:
         # Convert to OpenGL drawable VOpenGL
         shaderName = rawObject.shaderName
         return VObject(rawObject, self.__modelShader)
      else:
         return None

   def getDAEObject(self, filename:str):
      try:
         daeRawObject = RawObject()
         daeRawObject.loadDAE(filename)
         return VObject(daeRawObject, self.__modelShader)
      except Exception as ex:
         raise ex

   def getMap(self):
      try:
         rawMap = RawObject()
         rawMap.loadMap2(25, 1, "heightMap3.bmp", "earth2.jpg")
         return VMap(rawMap, MapShader())
      except Exception as ex:
         raise ex

   def getLightSource(self, name="testQuad.dae"):
      try:
         daeRawObject = RawObject()
         # Important! inverts normals to be a light
         daeRawObject.loadDAE("testQuad.dae", True)
         return VLightSource(daeRawObject, self.__modelShader)
      except Exception as ex:
         raise ex

   def getSkyBox(self, cubeMapName="skyBox"):
      try:
         rawCube = self.__dataController_o.getRawData("testCube")
         return VCubeMap(rawCube, CubeMapShader())
      except Exception as ex:
         raise ex