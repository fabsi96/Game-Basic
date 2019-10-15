# encoding: utf-8

from glm.gtc.matrix_transform import *
import math

from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DAL.Outer.vobject import VObject
from libs.OpenGL.Shader.NormalsShader.normalsshader import NormalsShader


class VMap(VObject):
   DIFFUSE_LIGHT_SPEED = 0.01
   def __init__(self, rawObject, mapShader):
      rawObject.textureFiles.append("blendMap.png")
      rawObject.textureFiles.append("stones.bmp")
      rawObject.textureFiles.append("grass.jpg")
      rawObject.textureFiles.append("mud.png")
      super(VMap, self).__init__(rawObject, mapShader)
      # --- Upload textures => pathMap and its compontents
      unitRunner = 0
      """
         Rot => Sand
         Blau => Pfad /- Straße
         Schwarz => Graß
      """
      self._uploadTexture("pathMap.bmp", "pathMapTexture", unitRunner)
      unitRunner += 1
      self._uploadTexture("grass.jpg", "grassTexture", unitRunner)
      unitRunner += 1
      self._uploadTexture("stones.bmp", "pathTexture", unitRunner)
      unitRunner += 1
      self._uploadTexture("mud.png", "sandTexture", unitRunner)
      unitRunner += 1


      # ---

      # Maps collision system
      self.colSystem = VCollisionSystem(self)
      # Objects on map (positioned by collision system)
      self.mapObjects = []
      self.mapHeights = rawObject.mapHeights
      self.mapSize = rawObject.mapSize
      self.mapVertexSize = rawObject.stepSize

   def addObject(self, vObject: VObject):
      self.mapObjects.append(vObject)

   def getHeight(self, x, z):
      try:
         # Check range of position
         if x > self.mapSize or z > self.mapSize or x < 0 or z < 0:
            return 0
         # Calculate nearest vertex
         mapHeight = -1
         restX = x % self.mapVertexSize
         restZ = z % self.mapVertexSize
         """
         minGridX = x - restX
         minGridZ = z - restZ
         nearestX = minGridX + round(restX)
         nearestZ = minGridZ + round(restZ)
         """
         minGridX = x - restX
         minGridZ = z - restZ
         maxGridX = minGridX + self.mapVertexSize
         maxGridZ = minGridZ + self.mapVertexSize
         hP1 = self.mapHeights[minGridZ][minGridX]
         hP2 = self.mapHeights[minGridZ][maxGridX]
         hP3 = self.mapHeights[maxGridZ][minGridX]
         hP4 = self.mapHeights[maxGridZ][maxGridX]
         if restX <= self.mapVertexSize - restZ:
            return RawObject.BarryCentric(tvec3([0.0, hP1, 0.0]),
                                          tvec3([self.mapVertexSize, hP2, 0.0]),
                                          tvec3([0.0, hP3, self.mapVertexSize]),
                                          tvec2([restX, restZ]))
         else:
            return RawObject.BarryCentric(tvec3([self.mapVertexSize, hP4, self.mapVertexSize]),
                                          tvec3([self.mapVertexSize, hP2, 0.0]),
                                          tvec3([0.0, hP3, self.mapVertexSize]),
                                          tvec2([restX, restZ]))
         # return x, self.mapHeights[nearestZ][nearestX], z
      except Exception as ex:
         raise ex


   def render(self):
      # Updating position of objects on map
      try:
         self.colSystem.update()
         # Then render map and its objects
         super(VMap, self).render()
         for mapObject in self.mapObjects:
            mapObject.render()
      except Exception as ex:
         print(str(ex))



class VCollisionSystem:
   def __init__(self, vMap: VMap):
      self.map = vMap

   def update(self):
      for obj in self.map.mapObjects:
         targetPos = obj.getPosition()
         y = self.map.getHeight(targetPos.x, targetPos.z)
         obj.setPosition(tvec3([targetPos.x, y, targetPos.z]))