# encoding: utf-8

# dal outer
from glm.gtc.matrix_transform import *

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
   def __init__(self, rawObject: RawObject, sp: ShaderProgram):
      super(VObject, self).__init__(rawObject, sp)

      self._position = tvec3([0.0, 0.0, -2.0])
      self._rotation = tvec3([1.0, 1.0, 1.0])
      self._degrees = float(0.0)
      self._scale = tvec3([1.0, 1.0, 1.0])
      self._transformationMatrix = tmat4x4([])
      self._updateTransformationMatrix()

      self.sp.loadMatrix4x4("transformMatrix")
      self.sp.loadMatrix4x4("projectionMatrix")
      self.sp.loadMatrix4x4("viewMatrix")

   def render(self):
      self.sp.start()
      glBindVertexArray(self.vao)
      glBindBuffer(GL_ARRAY_BUFFER, self.vertexVbo)

      self._updateTransformationMatrix()
      self.sp.setMatrix4x4("transformMatrix", self._transformationMatrix)
      self.sp.setMatrix4x4("projectionMatrix", np.matrix(Library.mainWindow.getProjectionMatrix(), dtype=np.float32))
      self.sp.setMatrix4x4("viewMatrix", np.matrix(Library.camera.getWorldToViewMatrix()))

      glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indicesVbo)
      for texture in self.textures:
         glActiveTexture(GL_TEXTURE0 + texture.unit)
         glBindTexture(GL_TEXTURE_2D, texture.vbo)
      glDrawElements(GL_TRIANGLES, self.indicesCount, GL_UNSIGNED_INT, None)
      glBindVertexArray(0)

      self.sp.stop()

   def _updateTransformationMatrix(self):
      self._transformationMatrix = translate(tmat4x4([]), self._position) * \
                                   rotate(tmat4x4([]), radians(self._degrees), self._rotation) * \
                                   scale(tmat4x4([]), self._scale)
      self._transformationMatrix = np.matrix(self._transformationMatrix, dtype=np.float32)

   def setPosition(self, x, y, z):
      self._position = tvec3([x, y, z])

   def setRotation(self, x, y, z, deg):
      self._rotation = tvec3([x, y, z])
      self._degrees = deg

   def setScale(self, x, y, z):
      self._scale = tvec3([x, y, z])

   def getPosition(self):
      return self._position

   def getRotation(self):
      return self._rotation, self._degrees

   def getScale(self):
      return self._scale

   def moveRight(self):
      self._position = tvec3([self._position.x + VObject.MOVEMENT_SPEED, self._position.y, self._position.z])

   def moveLeft(self):
      self._position = tvec3([self._position.x - VObject.MOVEMENT_SPEED, self._position.y, self._position.z])

   def moveUp(self):
      self._position = tvec3([self._position.x, self._position.y + VObject.MOVEMENT_SPEED, self._position.z])

   def moveDown(self):
      self._position = tvec3([self._position.x, self._position.y - VObject.MOVEMENT_SPEED, self._position.z])

