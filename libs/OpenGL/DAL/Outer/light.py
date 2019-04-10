# encoding: utf-8

from glm.gtc.matrix_transform import *
import numpy as np

from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DAL.Outer.vobject import VObject
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL
from libs.OpenGL.Shader.shaderprogram import ShaderProgram
from libs.library import Library


class VLight(VObject):
   def __init__(self, raw: RawObject, position: tvec3, shaderProgram: ShaderProgram):
      super(VLight, self).__init__(raw, shaderProgram)
      self._position = position

      """
         Light-test      
      """
      self._position = np.array(self._position, dtype=np.float32)
      self._lightColor = np.array(tvec3([0.5, 0.5, 0.5]), dtype=np.float32)
      try:
         self.sp.start()
         self.sp.loadVector3("lightPosition")
         self.sp.setVector3("lightPosition", self._position)
         self.sp.loadVector3("lightColor")
         self.sp.setVector3("lightColor", self._lightColor)
         self.sp.stop()
      except Exception as ex:
         print("shader ex :: {}".format(str(ex)))

   def render(self):
      super(VLight, self).render()