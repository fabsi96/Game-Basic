import sys
import os
import ctypes

from OpenGL.GL import *
import numpy as np
from glm import tvec3

"""
   DOC: 
   
   shaderprogram with its files, attribs names and ids, program/shader ids, 

   - implement files
   - implement error handling
"""

class ShaderProgram:
   positionName = "vertexCoord"
   colorName = "colorCoord"
   texturesName = "textureCoord"

   grayScaleTextureName = "grayScaleTexture"
   grassTextureName = "grassTexture"
   sandTextureName = "sandTexture"

   modelMatrixName = "modelMatrix"
   projectionMatrixName = "projectionMatrix"
   viewMatrixName = "viewMatrix"

   def __init__(self, shaderName: str, progID: int):

      self.__name = shaderName
      self.__programID = progID

      self.__attrIds = {}
      self.__matrixIds = {}
      self.__intIds = {}
      self.__floatIds = {}
      self.__texAttrIds = {}
      self.__vec3Ids = {}

   def getProgramID(self):
      return self.__programID

   def start(self):
      if self.__programID is None or self.__programID == -1:
         raise Exception("Shader program could not start. Check your shader sources.")
      else:
         glUseProgram(self.__programID)

   def stop(self):
      glUseProgram(0)

   def loadVertexAttribute(self, attrName: str):
      try:
         if self.__programID is not None and self.__programID != -1:
            index = glGetAttribLocation(self.__programID, attrName)
            if index == -1:
               raise Exception("Attribut konnte nicht geladen werden. Shader mal checken")
            self.__attrIds.update({attrName:index})
         else:
            raise Exception("")
      except Exception as ex:
         raise ex

   def setVertexAttribute(self, attrName: str, numVerts: int, vertType):
      index = self.__attrIds.get(attrName)
      if index is None or index == -1:
         raise Exception("Attribut konnte nicht gesetzt werden. Bitte Shader überprüfen.")
      else:
         glEnableVertexAttribArray(index)
         glVertexAttribPointer(index, numVerts, vertType, GL_FALSE, 0, None)

   def loadMatrix4x4(self, matrixName: str):
      try:
         if self.__programID is not None and self.__programID != -1:
            index = glGetUniformLocation(self.__programID, matrixName)
            if index == -1:
               raise Exception("Matrix konnte im Shader nicht gefunden werden.")
            self.__matrixIds.update({matrixName:index})
         else:
            raise Exception("Matrix konnte nicht geladen werden. Das Programm konnte nicht gestartet / geschweige denn gefunden werden.")
      except Exception as ex:
         raise ex

   def setMatrix4x4(self, matrixName: str, matrix: np.matrix):
      index = self.__matrixIds.get(matrixName)
      if index is None:
         raise Exception("Matrixname konnte nicht gefunden werden.")
      else:
         glUniformMatrix4fv(index, 1, GL_FALSE, matrix)

   def loadIntAttribute(self, attrName: str):
      try:
         if self.__programID is not None and self.__programID != -1:
            index = glGetAttribLocation(self.__programID, attrName)
            if index == -1:
               raise Exception("Attribut konnte nicht geladen werden.")
            self.__attrIds.update({attrName:index})
      except Exception as ex:
         raise ex
   def setIntAttribute(self, attrName: str, value: int):
      index = self.__attrIds.get(attrName)
      if index is None or index == -1:
         raise Exception("Attribut konnte nicht gesetzt werden.")
      else:
         glUniform1i(index, value)

   def loadFloatAttribute(self, attrName):
      try:
         if self.__programID is not None and self.__programID != -1:
            index = glGetAttribLocation(self.__programID, attrName)
            if index == -1:
               raise Exception("Attribut konnte nicht geladen werden.")
            self.__attrIds.update({attrName:index})
      except Exception as ex:
         raise ex

   def setFloatAttribute(self, attrName: str, value: float):
      index = self.__attrIds.get(attrName)
      if index is None or index == -1:
         raise Exception("Attribut konnte nicht gesetzt werden. Bitte Shader überprüfen.")
      else:
         glUniform1f(index, value)

   def loadTextureAttribute(self, attrName):
      try:
         if self.__programID and self.__programID != -1:
            index = glGetUniformLocation(self.__programID, attrName)
            if index == -1:
               raise Exception("Texturname konnte nicht gefunden werden. Bitte Shader auf Namen überprüfen.")
            else:
               self.__texAttrIds.update({attrName:index})
      except Exception as ex:
         raise ex

   def setTextureAttribute(self, attrName: str, value: int):
      index = self.__texAttrIds.get(attrName)
      if not index or index == -1:
         raise Exception("Texturename konnte nicht gefunden sowie nicht gesetzt werden. Bitte Shader überprüfen")
      else:
         glUniform1i(index, value)

   def loadVector3f(self, attrName: str):
      try:
         if self.__programID and self.__programID != -1:
            index = glGetUniformLocation(self.__programID, attrName)
            if index == -1:
               raise Exception("Vector3 konnte nicht gefunden werden. Bitte Shader auf Namen überprüfen.")
            else:
               self.__vec3Ids.update({attrName:index})
      except Exception as ex:
         raise ex

   def setVector3f(self, attrName: str, value: np.array):
      index = self.__vec3Ids.get(attrName)
      if index is None or index == -1:
         raise Exception("Vector3 konnte nicht gefunden sowie nicht gesetzt werden. Bitte Shader überprüfen")
      else:
         glUniform3fv(index, 1, value)

