# encoding: utf-8
from libs.OpenGL.DAL.Outer.vobject import VObject, tvec3


class VLightSource(VObject):
   def __init__(self, rawObject, sp):
      try:
         super(VLightSource, self).__init__(rawObject, sp)
         self.sp.addLightSource(self)
      except Exception as ex:
         print(str(ex))

   def setPosition(self, newPos: tvec3):
      super(VLightSource, self).setPosition(newPos)
      self.sp.updateLightSources()