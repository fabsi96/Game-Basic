import sys
import os
import ctypes
import weakref

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
   __refs__ = []

   positionName = "vertexCoord"
   colorName = "colorCoord"
   texturesName = "textureCoord"

   grayScaleTextureName = "grayScaleTexture"
   grassTextureName = "grassTexture"
   sandTextureName = "sandTexture"

   # Matrices
   modelMatrixName = "modelMatrix"
   projectionMatrixName = "projectionMatrix"
   viewMatrixName = "viewMatrix"

   # Light
   # Ambient
   AMBIENT_NAME = "ambientLight"

   # Diffuse
   DIFFUSE_NAME = "lightPosition"

   # Specular
   SPECULAR_NAME = ""

   # -----------------------------------------------
   def __init__(self, shaderName: str, progID: int):
   # -----------------------------------------------
      # Keep track of all class references
      self.__class__.__refs__.append(weakref.proxy(self))

      # Basic attributes
      self.__name = shaderName
      self.__programID = progID

      self.__attrIds = {}
      self.__matrixIds = {}
      self.__intIds = {}
      self.__floatIds = {}
      self.__texAttrIds = {}
      self.__vec3Ids = {}
      # -----------------------------------------------

      # Ambient light (basic groundcolor)
      # Will be set in EACH shader, that exist!
      self._ambientLightColor = tvec3([0.05, 0.05, 0.05])
      self._ambientLightShaderName = "ambientLight"
      self.setAmbientLight()

      # Diffuse Light
      # Array of objects (VLightSource)
      self._pointLights = []

      # TODO
      # Specular Light

      # -----------------------------------------------

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
               print("Attribut konnte nicht geladen werden. Shader mal checken")
            self.__attrIds.update({attrName:index})
         else:
            print("")
      except Exception as ex:
         raise ex
   def setVertexAttribute(self, attrName: str, numVerts: int, vertType):
      index = self.__attrIds.get(attrName)
      if index is None or index == -1:
         print("Attribut konnte nicht gesetzt werden. Bitte Shader überprüfen.")
      else:
         glEnableVertexAttribArray(index)
         glVertexAttribPointer(index, numVerts, vertType, GL_FALSE, 0, None)

   def loadMatrix4x4(self, matrixName: str):
      try:
         if self.__programID is not None and self.__programID != -1:
            index = glGetUniformLocation(self.__programID, matrixName)
            if index == -1:
               print("Matrix konnte im Shader nicht gefunden werden.")
            self.__matrixIds.update({matrixName:index})
         else:
            print("Matrix konnte nicht geladen werden. Das Programm konnte nicht gestartet / geschweige denn gefunden werden.")
      except Exception as ex:
         raise ex
   def setMatrix4x4(self, matrixName: str, matrix):
      index = self.__matrixIds.get(matrixName)
      if index is None:
         print("Matrixname konnte nicht gefunden werden.")
      else:
         glUniformMatrix4fv(index, 1, GL_FALSE, np.matrix(matrix, dtype=np.float32))

   def loadIntAttribute(self, attrName: str):
      try:
         if self.__programID is not None and self.__programID != -1:
            index = glGetUniformLocation(self.__programID, attrName)
            if index == -1:
               print("Attribut konnte nicht geladen werden.")
            self.__attrIds.update({attrName:index})
      except Exception as ex:
         raise ex
   def setIntAttribute(self, attrName: str, value: int):
      index = self.__attrIds.get(attrName)
      if index is None or index == -1:
         print("Attribut konnte nicht gesetzt werden.")
      else:
         glUniform1i(index, np.int(value))

   def loadFloatAttribute(self, attrName):
      try:
         if self.__programID is not None and self.__programID != -1:
            index = glGetAttribLocation(self.__programID, attrName)
            if index == -1:
               print("Attribut konnte nicht geladen werden.")
            self.__attrIds.update({attrName:index})
      except Exception as ex:
         raise ex
   def setFloatAttribute(self, attrName: str, value: float):
      index = self.__attrIds.get(attrName)
      if index is None or index == -1:
         print("Attribut konnte nicht gesetzt werden. Bitte Shader überprüfen.")
      else:
         glUniform1f(index, value)

   def loadTextureAttribute(self, attrName):
      try:
         if self.__programID and self.__programID != -1:
            index = glGetUniformLocation(self.__programID, attrName)
            if index == -1:
               print("Texturname konnte nicht gefunden werden. Bitte Shader auf Namen überprüfen.")
            else:
               self.__texAttrIds.update({attrName:index})
      except Exception as ex:
         raise ex
   def setTextureAttribute(self, attrName: str, value: int):
      index = self.__texAttrIds.get(attrName)
      if index is None or index == -1:
         print("Texturename konnte nicht gefunden sowie nicht gesetzt werden. Bitte Shader überprüfen")
      else:
         glUniform1i(index, value)

   def loadVector3f(self, attrName: str):
      try:
         if self.__programID and self.__programID != -1:
            index = glGetUniformLocation(self.__programID, attrName)
            if index == -1:
               print("Vector3 konnte nicht gefunden werden. Bitte Shader auf Namen überprüfen.")
            else:
               self.__vec3Ids.update({attrName:index})
      except Exception as ex:
         raise ex
   def setVector3f(self, attrName: str, value: np.array):
      index = self.__vec3Ids.get(attrName)
      if index is None or index == -1:
         print("Vector3 konnte nicht gefunden sowie nicht gesetzt werden. Bitte Shader überprüfen")
      else:
         glUniform3fv(index, 1, value)


   @staticmethod
   def setAmbientLight():
      """ Ambient light """
      try:
         for ref in ShaderProgram.__refs__:
            ref.start()
            ref.loadVector3f(ShaderProgram.AMBIENT_NAME)
            ref.setVector3f(ShaderProgram.AMBIENT_NAME, np.array(ref._ambientLightColor, dtype=np.float32))
            ref.stop()

      except Exception as ex:
         print("shader ex :: {}".format(str(ex)))

   @staticmethod
   def setAmbientLightColor(color: tvec3):
      for ref in ShaderProgram.__refs__:
         ref._ambientLightColor = color

   @staticmethod
   def setDiffuseLight():
      """ Diffuse light """
      try:
         for ref in ShaderProgram.__refs__:
            ref.start()
            # Light position
            ref.loadVector3f(ref._diffuseLightPositionShaderName)
            ref.setVector3f(ref._diffuseLightPositionShaderName, np.array(ref._diffuseLightPosition, dtype=np.float32))
            ref.stop()

      except Exception as ex:
         print("{}".format(str(ex)))
   """
   def setSpecularLight(self):
      try:
         self.start()
         self.loadVector3f("cameraPosition")
         self.setVector3f("cameraPosition", np.array(Library.camera.getPosition(), dtype=GLfloat))
         self.stop()

      except Exception as ex:
         raise ex

   def updateSpecularLight(self):
      try:
         if Library.camera is not None:
            self.loadVector3f("cameraPosition")
            self.setVector3f("cameraPosition", np.array(Library.camera.getPosition(), dtype=GLfloat))

      except Exception as ex:
         raise ex
   """
   def addLightSource(self, src):
      self._pointLights.append(src)
      self.updateLightSources()

   def updateLightSources(self):
      try:

         for ref in ShaderProgram.__refs__:
            # self.loadIntAttribute("currentAmountLights")
            # self.setIntAttribute("currentAmountLights", len(self._pointLights))

            ref.start()
            vecLoc = glGetUniformLocation(ref.__programID, "pointLights")
            pointLightPosArr = []
            for src in self._pointLights:
               pointLightPosArr.append(np.array(src.getPosition()))
            if vecLoc > -1:
               glUniform3fv(vecLoc, pointLightPosArr.__len__(), np.array(pointLightPosArr))
            else:
               print("Could not find 'pointLights' in shader")
            ref.stop()
      except Exception as ex:
         print("{} {} :: {}".format(self.__class__, __name__(), str(ex)))
