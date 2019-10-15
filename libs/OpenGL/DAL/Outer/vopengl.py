# encoding: utf-8

# libraries
import os
from abc import abstractmethod

from OpenGL.GL import *
import numpy as np

from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DataLoader.Texture.texture import Texture
from libs.OpenGL.Shader.shaderprogram import ShaderProgram


class VOpenGL:
   def __init__(self, rawObject: RawObject, sp: ShaderProgram):
      self.name = rawObject.name

      self.vertexCount = 0
      self.indicesCount = 0

      self.vao = None
      self.vertexVbo = None
      self.textureVbo = None
      self.normalVbo = None
      self.indicesVbo = None

      # TextureData
      self.textureFiles = rawObject.textureFiles
      self.textures = {}

      # Shaderprogram
      self.sp = sp
      try:
         self._uploadGeometry(rawObject)
      except Exception as ex:
         print(str(ex))

   @abstractmethod
   def render(self):
      raise NotImplementedError("Main Class")

   """ Returns vao and vbo """
   # -------------------------------
   @staticmethod
   def uploadVertexData(vao, data_f, shaderProgram, vertexShaderName, vertsPerCoord):
   # -------------------------------
      if vao is None or vao < 1:
         raise Exception("Vao is not defined")
      try:
         glBindVertexArray(vao)
         vbo = glGenBuffers(1)
         glBindBuffer(GL_ARRAY_BUFFER, vbo)
         numpyData = np.array(data_f, dtype=np.float32)
         glBufferData(GL_ARRAY_BUFFER, len(numpyData) * ctypes.sizeof(GLfloat), numpyData, GL_STATIC_DRAW)
         shaderProgram.loadVertexAttribute(vertexShaderName)
         shaderProgram.setVertexAttribute(vertexShaderName, vertsPerCoord, GL_FLOAT)
         glBindBuffer(GL_ARRAY_BUFFER, 0)
         glBindVertexArray(0)
         return vbo
      except Exception as ex:
         print(str(ex))
      return -1

   @staticmethod
   def uploadIndexData(vao, data_i):
      if vao is None or vao < 1:
         raise Exception("Vao is not defined.")

      try:
         glBindVertexArray(vao)
         vbo = glGenBuffers(1)
         glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo)
         indexData = np.array(data_i, dtype=GLuint)
         glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indexData) * ctypes.sizeof(GLuint), indexData, GL_STATIC_DRAW)
         glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
         glBindVertexArray(0)
         return vbo
      except Exception as ex:
         raise ex

   def _uploadGeometry(self, rawObject: RawObject):
      try:
         self.vao = glGenVertexArrays(1)
         glBindVertexArray(self.vao)
         if rawObject.vertexCoords.__len__() > 1:
            self.vertexVbo = VOpenGL.uploadVertexData(self.vao, rawObject.vertexCoords, self.sp, "vertexCoord", 3)
            self.vertexCount = len(rawObject.vertexCoords)
         if rawObject.indices.__len__() > 1:
            self.indicesVbo = VOpenGL.uploadIndexData(self.vao, rawObject.indices)
            self.indicesCount = len(rawObject.indices)
         if rawObject.normalCoords.__len__() > 1:
            self.normalVbo = VOpenGL.uploadVertexData(self.vao,rawObject.normalCoords, self.sp, "normalCoord", 3)
         if rawObject.textureCoords.__len__() > 1:
            self.textureVbo = VOpenGL.uploadVertexData(self.vao,rawObject.textureCoords, self.sp, "textureCoord", 2)
         glBindVertexArray(0)

      except Exception as ex:
         print("Exception :: {}".format(str(ex)))

   def _uploadTexture(self, filename, shaderTexName, unit):
      try:
         texture = Texture(filename, unit)
         if texture:
            self.sp.start()
            self.sp.loadTextureAttribute(shaderTexName)
            self.sp.setTextureAttribute(shaderTexName, unit)
            self.sp.stop()
            self.textures.update({texture:shaderTexName})

      except Exception as ex:
         raise ex
