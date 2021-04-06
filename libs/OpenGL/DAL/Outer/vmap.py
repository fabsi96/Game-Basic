# encoding: utf-8
import os

from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL
from libs.OpenGL.Shader.shaderprogram import ShaderProgram
from glm import *

# ---------------------------------------
class VMap(VOpenGL):
    """ Summary
    """
    DIFFUSE_LIGHT_SPEED = 0.01
    MAP_DATA_DIR = "data/res"

    # ---------------------------------------
    def __init__(self, rawObject: RawObject, mapShader: ShaderProgram):
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
        try:
            self._uploadTexture(os.path.join(VMap.MAP_DATA_DIR, "pathMap.bmp"), "pathMapTexture", unitRunner)
            unitRunner += 1
            self._uploadTexture(os.path.join(VMap.MAP_DATA_DIR, "grass.jpg"), "grassTexture", unitRunner)
            unitRunner += 1
            self._uploadTexture(os.path.join(VMap.MAP_DATA_DIR, "stones.bmp"), "pathTexture", unitRunner)
            unitRunner += 1
            self._uploadTexture(os.path.join(VMap.MAP_DATA_DIR, "mud.png"), "sandTexture", unitRunner)
            unitRunner += 1

            # Maps collision system
            self.colSystem = VCollisionSystem(self)
            # Objects on map (positioned by collision system)
            self.mapObjects = []
            self.mapHeights = rawObject.mapHeights
            self.mapSize = rawObject.mapSize
            self.mapVertexSize = rawObject.stepSize
        except Exception as ex:
            print(f"Not implemented exception. {self.__class__} {__name__} :: {str(ex)}")

    # ---------------------------------------
    def __uploadPathMapTextures(self, texFiles: dict) -> None:
        # TODO: Correct implementation
        try:
            for key, value in texFiles:
                print(f"Key / Value :: {key} / {value}")
        except Exception as ex:
            print(f"Not implemented exception. {self.__class__} {__name__} :: {str(ex)}")

    # ---------------------------------------
    def addVObject(self, newObject: VOpenGL) -> None:
        self.mapObjects.append(newObject)

    # ---------------------------------------
    def getHeight(self, x: float, z: float) -> float:
        try:
            # Check range of position
            if x > self.mapSize or z > self.mapSize or x < 0 or z < 0:
                return 0
            # Calculate nearest vertex
            restX = x % self.mapVertexSize
            restZ = z % self.mapVertexSize

            minGridX = x - restX
            minGridZ = z - restZ
            maxGridX = minGridX + self.mapVertexSize
            maxGridZ = minGridZ + self.mapVertexSize
            hP1 = self.mapHeights[minGridZ][minGridX]
            hP2 = self.mapHeights[minGridZ][maxGridX]
            hP3 = self.mapHeights[maxGridZ][minGridX]
            hP4 = self.mapHeights[maxGridZ][maxGridX]
            if restX <= self.mapVertexSize - restZ:
                return RawObject.BarryCentric(vec3([0.0, hP1, 0.0]),
                                              vec3([self.mapVertexSize, hP2, 0.0]),
                                              vec3([0.0, hP3, self.mapVertexSize]),
                                              vec2([restX, restZ]))
            else:
                return RawObject.BarryCentric(vec3([self.mapVertexSize, hP4, self.mapVertexSize]),
                                              vec3([self.mapVertexSize, hP2, 0.0]),
                                              vec3([0.0, hP3, self.mapVertexSize]),
                                              vec2([restX, restZ]))
        except Exception as ex:
            print(f"Not implemented exception. {self.__class__} {__name__} :: {str(ex)}")

    # ---------------------------------------
    def render(self) -> None:
        # Updating position of objects on map
        try:
            self.colSystem.update()
            # Then render map and its objects
            super(VMap, self).render()
            for mapObject in self.mapObjects:
                mapObject.render()
        except Exception as ex:
            print(f"Not implemented exception. {self.__class__} {__name__} :: {str(ex)}")


# -----------------------------
class VCollisionSystem:
    """ Summary
       Updates all objects on VMap with correct height
       * height
       * tilt (Neigung)
    """

    # -----------------------------
    def __init__(self, vMap: VMap):
        self.map = vMap

    # -----------------------------
    def update(self) -> None:
        for obj in self.map.mapObjects:
            targetPos = obj.getPosition()
            y = self.map.getHeight(targetPos.x, targetPos.z)
            heightOffset_f = 0.05
            obj.setPosition(vec3([targetPos.x, y + heightOffset_f, targetPos.z]))
