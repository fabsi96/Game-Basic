# encoding: utf-8
import numpy as np
import os
from xml.dom import minidom
from OpenGL.GL import *

class RawObject:
   VERTEXVERTICES = 3

   DATA_DIR = "data"
   def __init__(self):
      self.name = ""

      self.vertexCoords = []
      self.indices = []
      self.textureCoords = []
      self.normalCoords = []
      self.textureFiles = []

      self.shaderName = ""

   def loadDAE(self, filename: str):
      fullPath = os.path.join(RawObject.DATA_DIR, filename)
      if os.path.isfile(fullPath):
         xmlReader = minidom.parse("data/" + filename)
         if xmlReader is None:
            return

         # vertices
         dataItems = xmlReader.getElementsByTagName("float_array")
         modelVertices = []
         modelVerticesStr = None
         for item in dataItems:
            if item.attributes["id"].value == "Cube-mesh-positions-array":
               modelVerticesStr = item.firstChild.data
               break
         if modelVerticesStr is not None:
            modelVerticesStrArray = modelVerticesStr.split(" ")
            for i in range(0, len(modelVerticesStrArray)):
               modelVertices.append(float(modelVerticesStrArray[i]))
         # vertices

         # normals
         # TODO Implement normals
         modelNormals = []
         modelNormalsStr = None
         # normals

         # textures
         modelTextures = []
         modelTextureStr = ""
         for item in dataItems:
            # 1: Cube-mesh-map-0-array
            # 2: Cube_001-mesh-map-0-array
            if item.attributes["id"].value == "Cube-mesh-map-0-array":
               modelTextureStr = item.firstChild.data
               break
         modelTextureStrArray = modelTextureStr.split(" ")
         for i in range(0, len(modelTextureStrArray)):
            modelTextures.append(float(modelTextureStrArray[i]))
         # textures

         # indices
         indicesItem = xmlReader.getElementsByTagName("p")
         indicesStr = indicesItem[0].firstChild.data
         indicesStrArray = indicesStr.split(" ")
         modelIndices = []
         # TODO Implement modelNormalsIndices
         # --
         modelTexturesIndices = []
         for i in range(0, len(indicesStrArray), 4):
            modelIndices.append(int(indicesStrArray[i]))
            modelTexturesIndices.append(int(indicesStrArray[i + 2]))
         # indices


         modelVertices, modelNormals, modelTextures, modelIndices = self.sortVertices(modelVertices, modelNormals, modelTextures, modelIndices,
                                                                                      modelTexturesIndices)
         self.vertexCoords = np.array(modelVertices, dtype=np.float32)
         self.textureCoords = np.array(modelTextures, dtype=np.float32)
         self.indices = np.array(modelIndices, dtype=GLuint)

         # TODO
         self.name = filename
         self.textureFiles.append("characterTexture.png")

   def sortVertices(self, modelVertices, modelNormals, modelTextures, modelIndices, modelTextureIndices, modelNormalsIndices = None):
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

   def sortNormals(self):
      pass

   def sortTexture(self):
      pass

   def loadScaleMap(self, mapName: str):
      vertices = [0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0,
                  1.0, 0.0, 0.0,
                  1.0, 1.0, 0.0]
      normals = [0.0, 1.0, 0.0,
                 0.0, 1.0, 0.0,
                 0.0, 1.0, 0.0,
                 0.0, 1.0, 0.0]
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
