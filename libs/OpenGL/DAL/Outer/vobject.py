# encoding: utf-8

# dal outer
from glm.gtc.matrix_transform import *
from glm.gtc.quaternion import *
from glm.gtc.matrix_access import *

from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL

# libraries
from OpenGL.GL import *
import numpy as np

# Becomes OpenGL context informations
from libs.OpenGL.Shader.shaderprogram import ShaderProgram
from libs.library import Library


class VObject(VOpenGL):
   MOVEMENT_SPEED = 0.1
   def __init__(self, rawObject: RawObject, sp: ShaderProgram, normalsShader=None):
      try:
         super(VObject, self).__init__(rawObject, sp)
         self.renderMode = rawObject.renderMode

         # Translation
         self._position = tvec3([0.0, 0.0, -2.0])
         # Rotation
         self._xDegrees = 0
         self._yDegrees = 0
         self._zDegrees = 0
         # Scale
         self._scale = tvec3([1.0, 1.0, 1.0])
         # TransformationMatrix
         self._transformationMatrix = tmat4x4([1.0])
         self._updateTransformationMatrix()

         self.sp.loadMatrix4x4("transformMatrix")
         self.sp.loadMatrix4x4("projectionMatrix")
         self.sp.loadMatrix4x4("viewMatrix")

         """
            Visualize normals
         """
         if normalsShader is not None:
            self.__normalsShader = normalsShader
            self.__normalsShader.loadMatrix4x4("transformMatrix")
            self.__normalsShader.loadMatrix4x4("projectionMatrix")
            self.__normalsShader.loadMatrix4x4("viewMatrix")
            self.__vertexNormalsVAO = None
            self.__vertexNormalsVBO = None
            self.__vertexNormalsCount = -1
            self.__normalsVertices = VObject.calculateNormalsVertices(rawObject.vertexCoords, rawObject.normalCoords)
            self.__normalsVertices = np.array(self.__normalsVertices, dtype=np.float32)
            self.__vertexNormalsCount = int(len(self.__normalsVertices))
            self.__uploadNormalsVertices(self.__normalsVertices)

      except Exception as ex:
         print(str(ex))

   @staticmethod
   def calculateNormalsVertices(vertices, normals):
      normalsVertices = []
      try:
         for i in range(0, int(len(list(vertices))), 3):
            vVertices = [vertices[i], vertices[i+1], vertices[i+2]]
            vNormals = [normals[i], normals[i+1], normals[i+2]]

            normalsVertices.append(vVertices[0])
            normalsVertices.append(vVertices[1])
            normalsVertices.append(vVertices[2])
            normalsVertices.append(vVertices[0] + vNormals[0])
            normalsVertices.append(vVertices[1] + vNormals[1])
            normalsVertices.append(vVertices[2] + vNormals[2])
      except Exception as ex:
         raise ex

      return normalsVertices

   def __uploadNormalsVertices(self, normalsVertices):
      try:
         self.__vertexNormalsVAO = glGenVertexArrays(1)
         glBindVertexArray(self.__vertexNormalsVAO)
         self.__vertexNormalsVBO = glGenBuffers(1)
         glBindBuffer(GL_ARRAY_BUFFER, self.__vertexNormalsVBO)
         glBufferData(GL_ARRAY_BUFFER, len(normalsVertices) * ctypes.sizeof(GLfloat), normalsVertices, GL_STATIC_DRAW)
         self.__normalsShader.loadVertexAttribute("vertexCoord")
         self.__normalsShader.setVertexAttribute("vertexCoord", 3, GL_FLOAT)
         glBindBuffer(GL_ARRAY_BUFFER, 0)
         glBindVertexArray(0)
      except Exception as ex:
         raise ex

   def render(self):
      try:
         self.sp.start()
         glBindVertexArray(self.vao)
         glBindBuffer(GL_ARRAY_BUFFER, self.vertexVbo)
         # Has to be always on here
         glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

         self._updateTransformationMatrix()
         self.sp.setMatrix4x4("transformMatrix", self._transformationMatrix)
         self.sp.setMatrix4x4("projectionMatrix", np.matrix(Library.mainWindow.getProjectionMatrix(), dtype=np.float32))
         self.sp.setMatrix4x4("viewMatrix", np.matrix(Library.camera.getWorldToViewMatrix()))

         if self.renderMode == "ELEMENTS":
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indicesVbo)
            for texture in self.textures:
               glActiveTexture(GL_TEXTURE0 + texture.unit)
               glBindTexture(GL_TEXTURE_2D, texture.vbo)
            glDrawElements(GL_TRIANGLES, self.indicesCount, GL_UNSIGNED_INT, None)

         elif self.renderMode == "ARRAYS":
            for texture in self.textures:
               glActiveTexture(GL_TEXTURE0 + texture.unit)
               glBindTexture(GL_TEXTURE_2D, texture.vbo)
            glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

         else:
            raise Exception("Undefined render mode")

         glBindVertexArray(0)

         self.sp.stop()
      except Exception as ex:
         raise ex

   def renderNormalsVertices(self):
      try:
         """
            Visualize normals
         """
         self.__normalsShader.start()
         glBindVertexArray(self.__vertexNormalsVAO)
         glBindBuffer(GL_ARRAY_BUFFER, self.__vertexNormalsVBO)
         self._updateTransformationMatrix()
         self.__normalsShader.setMatrix4x4("transformMatrix", self._transformationMatrix)
         self.__normalsShader.setMatrix4x4("projectionMatrix",
                                           np.matrix(Library.mainWindow.getProjectionMatrix(), dtype=np.float32))
         self.__normalsShader.setMatrix4x4("viewMatrix", np.matrix(Library.camera.getWorldToViewMatrix()))

         # Define lines to draw
         glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
         glDrawArrays(GL_LINES, 0, self.__vertexNormalsCount)
         glBindBuffer(GL_ARRAY_BUFFER, 0)
         glBindVertexArray(0)
         self.__normalsShader.stop()

      except Exception as ex:
         raise ex

   def _updateTransformationMatrix(self):
      try:
         translationMatrix = translate(tmat4x4([1.0]), self._position)
         xRotationMatrix = rotate(translationMatrix, radians(self._xDegrees), tvec3([1.0, 0.0, 0.0]))
         yRotationMatrix = rotate(xRotationMatrix, radians(self._yDegrees), tvec3([0.0, 1.0, 0.0]))
         zRotationMatrix = rotate(yRotationMatrix, radians(self._zDegrees), tvec3([0.0, 0.0, 1.0]))
         self._transformationMatrix = scale(zRotationMatrix, self._scale)
         self._transformationMatrix = np.matrix(self._transformationMatrix, dtype=np.float32)
      except Exception as ex:
         raise ex

   def setPosition(self, newPos: tvec3):
      self._position = newPos

   def setXRotation(self, d):
      self._xDegrees = d

   def setYRotation(self, d):
      self._yDegrees = d

   def setZRotation(self, d):
      self._zDegrees = d

   def setScale(self, newScale: tvec3):
      self._scale = newScale

   def getPosition(self):
      return self._position

   def getXRotation(self):
      return self._xDegrees

   def getYRotation(self):
      return self._yDegrees

   def getZRotation(self):
      return self._zDegrees

   def getScale(self):
      return self._scale

   """ TODO Should be VPlayer-class """
   def moveRight(self):
      self._position = tvec3([self._position.x + VObject.MOVEMENT_SPEED, self._position.y, self._position.z])

   def moveLeft(self):
      self._position = tvec3([self._position.x - VObject.MOVEMENT_SPEED, self._position.y, self._position.z])

   def moveUp(self):
      self._position = tvec3([self._position.x, self._position.y + VObject.MOVEMENT_SPEED, self._position.z])

   def moveDown(self):
      self._position = tvec3([self._position.x, self._position.y - VObject.MOVEMENT_SPEED, self._position.z])
   """ TODO Should be VPlayer-class """
