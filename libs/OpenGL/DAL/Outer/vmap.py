# encoding: utf-8

from libs.OpenGL.DAL.Outer.vobject import VObject

class VMap(VObject):
   def __init__(self, rawObject, mapShader):
      super(VMap, self).__init__(rawObject, mapShader)

      self.mapObjects = []

   def addModel(self, model: VObject):
      self.mapObjects.append(model)

   def render(self):
      super(VMap, self).render()