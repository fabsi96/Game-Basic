# encoding: utf-8
from libs.OpenGL.DAL.Outer.vobject import VObject, tvec3


class VLightSource(VObject):
   def __init__(self, rawObject, sp):
      try:
         super(VLightSource, self).__init__(rawObject, sp)
         # X 0 - 1 on Z 2.5
         self.__xAnimationWay = 0
         self.__turnDirection = ""
      except Exception as ex:
         print(str(ex))

   def render(self):
      try:
         super(VLightSource, self).render()
         """
         if self.__xAnimationWay <= 0:
            self.__turnDirection = "right"
         elif self.__xAnimationWay >= 5:
            self.__turnDirection = "left"
         else:
            pass
         """

         if self.__turnDirection == "right":
            self.__xAnimationWay += 0.01
         elif self.__turnDirection == "left":
            self.__xAnimationWay -= 0.01
         else:
            pass
         # self.setPosition(tvec3([self.__xAnimationWay, self.getPosition().y, self.getPosition().z]))

      except Exception as ex:
         raise ex


   def setPosition(self, newPos: tvec3):
      super(VLightSource, self).setPosition(newPos)
      self.sp.setLightPosition(tvec3([newPos.x, newPos.y + 0.25, newPos.z]))