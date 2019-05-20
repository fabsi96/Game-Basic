# encoding: utf-8

import numpy as np
import os
from OpenGL.GL import *
from PIL import Image
from collada import Collada
from glm.gtc.matrix_transform import *

class RawObject:
   VERTEXVERTICES = 3
   MAX_HEIGHT = 2
   MAX_PIXEL_COMPONENT = 256
   MAX_PIXEL_COLOR = MAX_PIXEL_COMPONENT * MAX_PIXEL_COMPONENT * MAX_PIXEL_COMPONENT

   DATA_DIR = "data"
   def __init__(self):
      self.name = ""
      self.renderMode = "ELEMENTS"

      self.vertexCoords = []
      self.indices = []
      self.textureCoords = []
      self.normalCoords = []
      self.textureFiles = []

      self.shaderName = ""

      self.mapSize = -1
      self.mapHeights = {}

   def loadDAE(self, filename: str):
      fullPath = os.path.join(RawObject.DATA_DIR, filename)
      if os.path.isfile(fullPath):
         modelVertices = []
         modelIndices = []

         modelNormals = []
         modelNormalsIndices = []
         modelTextures = []
         modelTexturesIndices = []

         daeVertices = []
         daeIndices = []
         daeNormals = []
         daeNormalsIndices = []
         daeTextures = []
         daeTexturesIndices = []

         try:
            dae = Collada(os.path.join("data", filename))
            modelImages = []
            for texFile in dae.images:
               modelImages.append(texFile.path)
            for geom in dae.geometries:
               daeVertices = geom.primitives[0].vertex.tolist()
               daeIndices = list(geom.primitives[0].vertex_index)

               daeNormals = geom.primitives[0].normal.tolist()
               daeNormalsIndices = list(geom.primitives[0].normal_index)

               daeTextures = geom.primitives[0].texcoordset[0].tolist()
               daeTexturesIndices = list(geom.primitives[0].texcoord_indexset[0])


         except Exception as ex:
            raise ex
         modelVertices.clear()
         for i in daeVertices:
            modelVertices.append(i[0])
            modelVertices.append(i[1])
            modelVertices.append(i[2])
         for i in daeNormals:
            modelNormals.append(i[0])
            modelNormals.append(i[1])
            modelNormals.append(i[2])
         for data in daeTextures:
            modelTextures.append(data[0])
            modelTextures.append(data[1])


         if type(daeIndices[0]) is not np.ndarray and type(daeIndices[0]) is not list:
            modelIndices = daeIndices
            modelNormalsIndices = daeNormalsIndices
            modelTexturesIndices = daeTexturesIndices
         else:
            for data in daeIndices:
               modelIndices.append(data[0])
               modelIndices.append(data[1])
               modelIndices.append(data[2])
            for data in daeNormalsIndices:
               modelNormalsIndices.append(data[0])
               modelNormalsIndices.append(data[1])
               modelNormalsIndices.append(data[2])
            for data in daeTexturesIndices:
               modelTexturesIndices.append(data[0])
               modelTexturesIndices.append(data[1])
               modelTexturesIndices.append(data[2])

         modelVertices, modelNormals, modelTextures = RawObject.triangulateDaeIndices(modelVertices, modelNormals,
                                                                                      modelTextures,
                                                                                      modelIndices, modelNormalsIndices,
                                                                                      modelTexturesIndices)

         self.vertexCoords = np.array(modelVertices, dtype=np.float32)
         self.normalCoords = np.array(modelNormals, dtype=np.float32)
         self.textureCoords = np.array(modelTextures, dtype=np.float32)
         # self.indices = np.array(modelIndices, dtype=GLuint)
         self.renderMode = "ARRAYS"

         self.name = filename
         self.textureFiles = modelImages

   @staticmethod
   def sortVertices(modelVertices, modelNormals, modelTextures, modelIndices, modelTextureIndices, modelNormalsIndices = None):
      processedIndices = []
      newModelTextures = []
      for i in range(0, len(modelTextures)):
         newModelTextures.append(0)

      for i in range(0, int(len(modelTextures) / 2)):
         vIndex = modelIndices[i]
         tIndex = modelTextureIndices[i]

         exists = False
         for j in range(0, len(processedIndices)):
            if processedIndices[j] == vIndex:
               exists = True

         if not exists:
            targetTextureCoord = [modelTextures[(tIndex * 2)], modelTextures[(tIndex * 2) + 1]]
            tmpTextureCoord = [modelTextures[(vIndex * 2)], modelTextures[(vIndex * 2) + 1]]
            newModelTextures[(vIndex * 2)] = targetTextureCoord[0]
            newModelTextures[(vIndex * 2) + 1] = targetTextureCoord[1]
            modelTextures[(tIndex * 2)] = tmpTextureCoord[0]
            modelTextures[(tIndex * 2) + 1] = tmpTextureCoord[1]
            processedIndices.append(vIndex)
         else:
            targetTextureCoord = [modelVertices[(vIndex * 3)], modelVertices[(vIndex * 3) + 1], modelVertices[(vIndex * 3) + 2]]

            modelVertices.append(targetTextureCoord[0])
            modelVertices.append(targetTextureCoord[1])
            modelVertices.append(targetTextureCoord[2])

            newIndex = int(((len(modelVertices) + 3) / 3)) - 2

            modelIndices[i] = newIndex


            newModelTextures[(newIndex * 2)] = modelTextures[(tIndex * 2)]
            newModelTextures[(newIndex * 2) + 1] = modelTextures[(tIndex * 2) + 1]

      return modelVertices, modelNormals, newModelTextures, modelIndices
   # TODO
   def sortNormals(self):
      pass
   # TODO
   def sortTexture(self):
      pass
   @staticmethod
   def triangulateDaeIndices(modelVertices, modelNormals, modelTextures, modelVerticesIndex, modelNormalsIndex, modelTexturesIndex):
      newModelVertices = []
      newModelNormals = []
      newModelTextures = []

      # Implied that model have more texture coords than others
      for i in range(0, len(modelVerticesIndex)): #)-(3*1256)
         # 0, 1, 2, ... point-for-point (punkt für punkt)
         currentVertex  = [modelVertices[modelVerticesIndex[i]*3], modelVertices[modelVerticesIndex[i]*3+1], modelVertices[modelVerticesIndex[i]*3+2]]
         currentNormal  = [modelNormals[modelNormalsIndex[i]*3], modelNormals[modelNormalsIndex[i]*3+1], modelNormals[modelNormalsIndex[i]*3+2]]
         currentTexture = [modelTextures[modelTexturesIndex[i]*2], modelTextures[modelTexturesIndex[i]*2+1]]
         for v in currentVertex:
            newModelVertices.append(v)
         for n in currentNormal:
            newModelNormals.append(n)
         for t in currentTexture:
            newModelTextures.append(t)


      return newModelVertices, newModelNormals, newModelTextures

   def loadScaleMap(self, mapName: str):
      vertices = [0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0,
                  1.0, 0.0, 0.0,
                  1.0, 1.0, 0.0]
      normals = [0.0, 0.0, -1.0,
                 0.0, 0.0, -1.0,
                 0.0, 0.0, -1.0,
                 0.0, 0.0, -1.0]
      textures = [0.0, 0.0,
                  0.0, 1.0,
                  1.0, 0.0,
                  1.0, 1.0]
      indices = [0, 1, 2, 1, 3, 2]

      self.vertexCoords = np.array(vertices, dtype=np.float32)
      self.normalCoords = np.array(normals, dtype=np.float32)
      self.textureCoords = np.array(textures, dtype=np.float32)
      self.indices = np.array(indices, dtype=GLuint)

      # TODO
      self.name = mapName
      self.textureFiles.append("mud.png")

   @staticmethod
   def BarryCentric(p1: tvec3, p2: tvec3, p3: tvec3, pos: tvec2):
      det = (p2.z - p3.z) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.z - p3.z)
      l1 = ((p2.z - p3.z) * (pos.x - p3.x) + (p3.x - p2.x) * (pos.y - p3.z)) / det
      l2 = ((p3.z - p1.z) * (pos.x - p3.x) + (p1.x - p3.x) * (pos.y - p3.z)) / det
      l3 = 1.0 - l1 - l2
      return l1 * p1.y + l2 * p2.y + l3 * p3.y

   def loadMap(self, mapSize, mapDividor, heightMapFilename, pathMapFilename):
      self.mapHeights = {}
      self.mapSize = mapSize

      vertices = []
      textures = []
      indices = []
      size = mapSize
      dividor = mapDividor
      heightMapFilename = heightMapFilename
      # load image
      image = Image.open("data/res/" + heightMapFilename)

      # check size gerade und dividor 2^n
      polyFactor = size / dividor
      i = 0
      j = 0
      while i <= size:
         self.mapHeights[i] = {}
         while j <= size:
            # Multi-mapped
            div = image.width / mapSize
            xCoord = int(j * div)
            yCoord = int(i * div)
            # --
            height = self.__getHeight(image, xCoord, yCoord)
            vertices.append(j)  # x
            vertices.append(0.0)  # y
            vertices.append(i)  # z
            self.mapHeights[i][j] = height

            textures.append(j / size)
            textures.append(i / size)
            j += polyFactor
         j = 0
         i += polyFactor
      runner = 0
      for k in range(0, dividor - 1):
         for l in range(0, dividor - 1):
            indices.append(runner)
            indices.append(runner + 1)
            indices.append(runner + 2 + dividor)

            indices.append(runner)
            indices.append(runner + dividor + 1)
            indices.append(runner + dividor + 2)
            runner += 1
         runner += 2


      self.vertexCoords = vertices
      self.textureCoords = textures
      self.indices = indices
      self.renderMode = "ELEMENTS"
      self.textureFiles.append(pathMapFilename)

   def __getHeight(self, image: Image, x: int, y: int):
      if x < 0 or x >= image.width or y < 0 or y >= image.height:
         return 0
      try:
         r, g, b = image.getpixel((x, y))
      except:
         print("Range value : {0}/{1}".format(x, y))
      height = r * g * b
      height = -height
      height += self.MAX_PIXEL_COLOR / 2.0
      height /= self.MAX_PIXEL_COLOR / 2.0
      height *= self.MAX_HEIGHT

      return height

   def loadMap2(self, mapSize=10, mapDividor=8):
      # load image
      image = Image.open("data/res/" + "hmap.bmp")

      # Geometry helper
      stepSize = 1 / mapDividor
      x = 0
      z = 0
      while z <= mapSize:
         while x <= mapSize:
            self.vertexCoords.append(x)
            self.vertexCoords.append(self.__getHeight2(image, mapSize, x, z))
            self.vertexCoords.append(z)
            x = x + stepSize
         x = 0
         z = z + stepSize

      vertexCountPerSite = int(mapSize / stepSize)
      i = 0
      runner = 0
      j = 0
      # Indices works
      while j <= vertexCountPerSite-1:
         while i <= vertexCountPerSite-1:
            self.indices.append(runner + vertexCountPerSite + 1)
            self.indices.append(runner + 1)
            self.indices.append(runner)

            self.indices.append(runner + vertexCountPerSite + 1)
            self.indices.append(runner + vertexCountPerSite + 2)
            self.indices.append(runner + 1)

            i = i + 1
            runner = runner + 1

         j = j + 1
         runner = runner + 1
         i = 0

   def __getHeight2(self, image: Image, mapSize, x, z):
      # Convert map-coordinates to image coords
      imageWidth = image.width
      imageHeight = image.height
      imageX = 0
      imageY = 0
      if x != 0:
         imageX = (x / (mapSize+1)) * imageWidth
      if z != 0:
         imageY = (z / (mapSize+1)) * imageHeight
      try:
         r, g, b = image.getpixel((imageX, imageY))
      except:
         print("Range value : {0}/{1}".format(imageX, imageY))
      height = r * g * b
      height = -height
      height += self.MAX_PIXEL_COLOR / 2.0
      height /= self.MAX_PIXEL_COLOR / 2.0
      height *= self.MAX_HEIGHT

      return height
