# encoding: utf-8

# libraries
from abc import abstractmethod

from OpenGL.GL import *

from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DataLoader.Texture.texture import Texture
from libs.OpenGL.Shader.shaderprogram import ShaderProgram


class VOpenGL:
   def __init__(self, rawObject: RawObject, sp: ShaderProgram):
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

      self._uploadGeometry(rawObject)

   @abstractmethod
   def render(self):
      raise NotImplementedError("Main Class")

   def _uploadGeometry(self, rawObject: RawObject):

      try:
         self.vao = glGenVertexArrays(1)
         glBindVertexArray(self.vao)
         if rawObject.vertexCoords.__len__() > 1:
            self._uploadVertices(rawObject.vertexCoords)
         if rawObject.indices.__len__() > 1:
            self._uploadIndices(rawObject.indices)
         if rawObject.normalCoords.__len__() > 1:
            self._uploadNormals(rawObject.normalCoords)
         if rawObject.textureCoords.__len__() > 1:
            self._uploadTextures(rawObject.textureCoords)

         for texFile in self.textureFiles:
            self._uploadTexture(texFile, "testTexture", 0)
         glBindVertexArray(0)

      except Exception as ex:
         print("Exception :: {}".format(str(ex)))

   def _uploadVertices(self, vertices):
      try:
         self.vertexVbo = glGenBuffers(1)
         glBindBuffer(GL_ARRAY_BUFFER, self.vertexVbo)
         glBufferData(GL_ARRAY_BUFFER, len(vertices) * ctypes.sizeof(GLfloat), vertices, GL_STATIC_DRAW)
         self.sp.loadVertexAttribute("vertexCoord")
         self.sp.setVertexAttribute("vertexCoord", 3, GL_FLOAT)
         glBindBuffer(GL_ARRAY_BUFFER, 0)

      except Exception as ex:
         raise ex

   def _uploadIndices(self, indices):
      try:
         self.indicesCount = int(len(indices))
         self.indicesVbo = glGenBuffers(1)
         glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indicesVbo)
         glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * ctypes.sizeof(GLuint), indices, GL_STATIC_DRAW)
         glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
      except Exception as ex:
         raise ex
   def _uploadNormals(self, normals):
      try:
         self.normalVbo = glGenBuffers(1)
         glBindBuffer(GL_ARRAY_BUFFER, self.normalVbo)
         glBufferData(GL_ARRAY_BUFFER, len(normals) * ctypes.sizeof(GLfloat), normals, GL_STATIC_DRAW)
         self.sp.loadVertexAttribute("normalCoord")
         self.sp.setVertexAttribute("normalCoord", 3, GL_FLOAT)
         glBindBuffer(GL_ARRAY_BUFFER, 0)

      except Exception as ex:
         raise ex
   def _uploadTextures(self, textures):
      try:
         self.textureVbo = glGenBuffers(1)
         glBindBuffer(GL_ARRAY_BUFFER, self.textureVbo)
         glBufferData(GL_ARRAY_BUFFER, len(textures) * ctypes.sizeof(GLfloat), textures, GL_STATIC_DRAW)
         self.sp.loadVertexAttribute("textureCoord")
         self.sp.setVertexAttribute("textureCoord", 2, GL_FLOAT)
         glBindBuffer(GL_ARRAY_BUFFER, 0)

      except Exception as ex:
         raise ex
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
