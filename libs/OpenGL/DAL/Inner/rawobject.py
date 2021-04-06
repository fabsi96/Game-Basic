# encoding: utf-8
from datetime import datetime
from glm import *

from PIL import Image
from pyassimp import *
# -----------------
from pyassimp.postprocess import *
from pyassimp.structs import *


# -----------------
class RawObject:
    """ Summary
       Loads OpenGL Data into RAM. Specific arrays (numpy-arrays)
       Always 'returns' itself as data-object.
    """
    VERTEXVERTICES = 3
    MAX_HEIGHT = 1.5
    MAX_PIXEL_COMPONENT = 256
    MAX_PIXEL_COLOR = MAX_PIXEL_COMPONENT * MAX_PIXEL_COMPONENT * MAX_PIXEL_COMPONENT

    # -----------------
    def __init__(self):
        self.name = ""
        self.renderMode = ""

        """ Single vertex objects """
        self.vertexCoords = []
        self.indices = []
        self.textureCoords = []
        self.normalCoords = []
        self.textureFiles = []

        """ Multiple meshes objects """
        self.verticesMeshes = []
        self.normalsMeshes = []
        self.texturesMeshes = []
        self.textureFilesMeshes = []
        self.indicesMeshes = []

        self.shaderName = ""

        """ Map - attributes """
        self.mapSize = -1
        self.mapHeights = {}
        self.stepSize = -1

    def loadCube(self, SIZE=100):
        self.vertexCoords = [
            -SIZE, SIZE, -SIZE,
            -SIZE, -SIZE, -SIZE,
            SIZE, -SIZE, -SIZE,
            SIZE, -SIZE, -SIZE,
            SIZE, SIZE, -SIZE,
            -SIZE, SIZE, -SIZE,

            -SIZE, -SIZE, SIZE,
            -SIZE, -SIZE, -SIZE,
            -SIZE, SIZE, -SIZE,
            -SIZE, SIZE, -SIZE,
            -SIZE, SIZE, SIZE,
            -SIZE, -SIZE, SIZE,

            SIZE, -SIZE, -SIZE,
            SIZE, -SIZE, SIZE,
            SIZE, SIZE, SIZE,
            SIZE, SIZE, SIZE,
            SIZE, SIZE, -SIZE,
            SIZE, -SIZE, -SIZE,

            -SIZE, -SIZE, SIZE,
            -SIZE, SIZE, SIZE,
            SIZE, SIZE, SIZE,
            SIZE, SIZE, SIZE,
            SIZE, -SIZE, SIZE,
            -SIZE, -SIZE, SIZE,

            -SIZE, SIZE, -SIZE,
            SIZE, SIZE, -SIZE,
            SIZE, SIZE, SIZE,
            SIZE, SIZE, SIZE,
            -SIZE, SIZE, SIZE,
            -SIZE, SIZE, -SIZE,

            -SIZE, -SIZE, -SIZE,
            -SIZE, -SIZE, SIZE,
            SIZE, -SIZE, -SIZE,
            SIZE, -SIZE, -SIZE,
            -SIZE, -SIZE, SIZE,
            SIZE, -SIZE, SIZE]

    DATA_DAE_DIR = "data/dae"

    # -----------------
    def loadDAE(self, filename: str, isLight=False) -> int:
        fullPath_s = os.path.join(RawObject.DATA_DAE_DIR, filename)
        if not os.path.isfile(fullPath_s):
            return -1

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

        # Load data from .dae - file
        modelImages = []

        try:
            """
                Parts := shape_o.meshes
                vertices := shape_o.meshes[i].vertices
                normals := shape_o.meshes[i].normals
                vertices := shape_o.meshes[i].texturecoords
                indices := shape_o.meshes[i].faces
                textureFiles := shape_o.textures
            """
            shape_o: Scene = load(filename=fullPath_s, processing=aiProcess_Triangulate)

            # Load only the first mesh into memory
            for currShape in shape_o.meshes:
                daeVertices = currShape.vertices
                daeNormals = currShape.normals
                daeTextures = currShape.texturecoords
                daeIndices = currShape.faces
                break

            # TODO: Correct material loading (images)
            for material in shape_o.materials:
                pass
                # print(f"Material :: {material}")
                """
                for key,value in material.properties.items():
                    # print(f"Key {key} / Value {value}")
                    if key == "file":
                        modelImages.append(value)
                """

            # Vertices -> DAE transformation Blender -> OpenGL ???
            for i in daeVertices:
                modelVertices.append(i[0])  # x
                modelVertices.append(i[2])  # y
                modelVertices.append(i[1])  # z

            # Normals
            for i in daeNormals:
                if isLight is True:
                    # TODO: Correct normal calculaton
                    modelNormal = vec3(i[0], i[1], i[2])
                    modelNormals.append(modelNormal.x * -1)
                    modelNormals.append(modelNormal.y * -1)
                    modelNormals.append(modelNormal.z * -1)
                else:
                    modelNormals.append(i[0])
                    modelNormals.append(i[2])
                    modelNormals.append(i[1])

            # Textures
            for data in daeTextures:
                for textureVertex in data:
                    modelTextures.append(textureVertex[0])
                    modelTextures.append(textureVertex[1])

            # Clean up loaded scene
            release(shape_o)

        except AssimpError as ex:
            print(f"loadDAE: RawObject [ERROR] Assimp exception {ex.args}")
            return -1

        except Exception as ex:
            print(f"loadDAE: RawObject [ERROR] {ex.args}")
            return -1

        try:
            # --- Summarize all data
            self.vertexCoords = modelVertices
            self.normalCoords = modelNormals
            self.textureCoords = modelTextures
            if len(modelIndices) > 0:
                self.indices = modelIndices
                self.renderMode = "ELEMENTS"
            else:
                self.renderMode = "ARRAYS"
            self.name = fullPath_s
            self.textureFiles = modelImages
            if self.textureFiles.__len__() == 0:
                self.textureFiles.append("path.jpg")

            """
            beforeLoading_o = datetime.now()
            afterLoading_o = datetime.now()
            loadingTime_o = afterLoading_o - beforeLoading_o
            loadingTime_seoncds = loadingTime_o.total_seconds()
            print(f"loadMap: RawObject [DEBUG] ('' Mb / '{loadingTime_seoncds}' sec) ")
            """
            return 1

        except Exception as ex:
            print(f"loadDAE: RawObject [ERROR] {ex.args}")
            return -1

    def loadBlenderMultipleParts(self, filename_s: str, textureFiles_l: list):
        fullPath_s = os.path.join(RawObject.DATA_DAE_DIR, filename_s)
        if not os.path.isfile(fullPath_s):
            return -1

        modelVertices = []
        modelNormals = []
        modelTextures = []
        modelIndices = []

        # Load data from .dae - file
        modelImages = []

        try:
            print(f"loadBlenderMultipleParts: RawObject [DEBUG] Loading '{fullPath_s}'")
            import datetime
            before = datetime.datetime.now()
            shape_o: Scene = load(filename=fullPath_s, processing=aiProcess_FlipUVs |
                                                                  aiProcess_GenNormals |
                                                                  aiProcess_Triangulate)
            after = datetime.datetime.now()
            elapsedTime = after - before
            elapsedSeconds_f = elapsedTime.total_seconds()
            print(f"loadBlenderMultipleParts: RawObject [DEBUG] Elapsed time {elapsedSeconds_f}")

            meshVertices = []
            meshNormals = []
            meshTextures = []
            meshIndices = []
            for currShape in shape_o.meshes:
                meshVertices = currShape.vertices
                meshNormals = currShape.normals
                meshTextures = currShape.texturecoords
                meshIndices = currShape.faces

                # Vertices -> DAE transformation Blender -> OpenGL ???
                for i in meshVertices:
                    modelVertices.append(i[0])  # x
                    modelVertices.append(i[2])  # y
                    modelVertices.append(i[1])  # z
                self.verticesMeshes.append(list(modelVertices))
                modelVertices.clear()

                # Normals
                for i in meshNormals:
                    modelNormals.append(i[0])
                    modelNormals.append(i[2])
                    modelNormals.append(i[1])
                self.normalsMeshes.append(list(modelNormals))
                modelNormals.clear()

                # Textures
                for data in meshTextures:
                    for textureVertex in data:
                        modelTextures.append(textureVertex[0])
                        modelTextures.append(textureVertex[1])
                self.texturesMeshes.append(list(modelTextures))
                modelTextures.clear()

                # Indices
                self.indicesMeshes.append(meshIndices)

                # END Mesh[i]

            # Clean up loaded scene
            release(shape_o)

        except AssimpError as ex:
            print(f"loadDAE: RawObject [ERROR] Assimp exception {ex.args}")
            return -1

        except Exception as ex:
            print(f"loadDAE: RawObject [ERROR] {ex.args}")
            return -1

        try:
            # --- Summarize all data
            self.vertexCoords = modelVertices
            self.normalCoords = modelNormals
            self.textureCoords = modelTextures
            self.renderMode = "ELEMENTS"
            self.name = fullPath_s
            self.textureFiles = textureFiles_l

            return 1

        except Exception as ex:
            print(f"loadDAE: RawObject [ERROR] {ex.args}")
            return -1

    # -----------------
    @staticmethod
    def BarryCentric(p1: vec3, p2: vec3, p3: vec3, pos: vec2) -> float:
        det = (p2.z - p3.z) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.z - p3.z)
        l1 = ((p2.z - p3.z) * (pos.x - p3.x) + (p3.x - p2.x) * (pos.y - p3.z)) / det
        l2 = ((p3.z - p1.z) * (pos.x - p3.x) + (p1.x - p3.x) * (pos.y - p3.z)) / det
        l3 = 1.0 - l1 - l2
        return l1 * p1.y + l2 * p2.y + l3 * p3.y

    DATA_HEIGHT_MAPS_DIR = "data/res/height_maps"
    DATA_PATH_MAPS_DIR = "data/res/path_maps"

    # -----------------
    def loadMap(self, mapSize=10, mapDividor=1, heightMap="", pathMap="") -> int:
        if mapDividor > 16:
            # print(f"loadMap: RawObject [ERROR] Too high mapdividor")
            return -1

        fullHeightMapPath_s = os.path.join(RawObject.DATA_HEIGHT_MAPS_DIR, heightMap)
        isHeightMapFile = os.path.isfile(fullHeightMapPath_s)
        image = None
        if isHeightMapFile:
            image = Image.open(fullHeightMapPath_s)
        else:
            # print(f"loadMap: RawObject [DEBUG] Could not find height map.")
            pass

        fullPathMapPath_s = os.path.join(RawObject.DATA_PATH_MAPS_DIR, pathMap)
        isPathFile = os.path.isfile(fullPathMapPath_s)
        if isPathFile:
            self.textureFiles.append(pathMap)
        else:
            # print(f"loadMap: RawObject [DEBUG] Could not find pathmap.")
            pass

        # Geometry helper
        stepSize = 1 / mapDividor
        xRunner = 0
        zRunner = 0
        while zRunner <= mapSize:
            self.mapHeights[zRunner] = {}
            while xRunner <= mapSize:
                """ Calculate height at this point """
                roundedHeight_f = 0.0
                currentNormal = vec3(0.0, 1.0, 0.0)
                if image is not None:
                    height_f = float(self.__getHeight(image, mapSize, xRunner, zRunner))
                    roundedHeight_s = "{:.5f}".format(height_f)
                    roundedHeight_f = float(roundedHeight_s)
                    currentNormal: vec3 = self.__calcNormal(image, mapSize, xRunner, zRunner)

                self.vertexCoords.append(xRunner)
                self.vertexCoords.append(roundedHeight_f)
                self.vertexCoords.append(zRunner)
                self.mapHeights[zRunner][xRunner] = roundedHeight_f

                self.normalCoords.append(currentNormal.x)
                self.normalCoords.append(currentNormal.y)
                self.normalCoords.append(currentNormal.z)

                self.textureCoords.append((xRunner / (mapSize + 1)))  # x
                self.textureCoords.append((zRunner / (mapSize + 1)))  # y

                xRunner = xRunner + stepSize
            xRunner = 0
            zRunner = zRunner + stepSize

        vertexCountPerSite = int(mapSize / stepSize)
        i = 0
        runner = 0
        j = 0
        # Indices works
        while j <= vertexCountPerSite - 1:
            while i <= vertexCountPerSite - 1:
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

            self.stepSize = stepSize
            self.mapSize = mapSize

        return 1

    # -----------------
    def __getHeight(self, image: Image, mapSize: int, xCoord: float, zCoord: float) -> float:
        # Convert map-coordinates to image coords
        imageWidth = image.width - 1
        imageHeight = image.height - 1
        if xCoord >= 0 and zCoord >= 0:
            imageX = (xCoord / (mapSize + 1)) * imageWidth
            imageY = (zCoord / (mapSize + 1)) * imageHeight
            try:
                r, g, b = image.getpixel((imageX, imageY))
                return (r * g * b) * self.MAX_HEIGHT / self.MAX_PIXEL_COLOR * -1
            except Exception as ex:
                print("{} :: Range value : {}/{}".format(self.__class__, imageX, imageY))

        else:
            return 0

    # -----------------
    def __calcNormal(self, image: Image, mapSize: int, x: float, z: float) -> vec3:
        hLeft = self.__getHeight(image, mapSize, x - 1, z)
        hRight = self.__getHeight(image, mapSize, x + 1, z)
        hDown = self.__getHeight(image, mapSize, x, z - 1)
        hUp = self.__getHeight(image, mapSize, x, z + 1)

        normal = vec3([hLeft - hRight, 2.0, hDown - hUp])

        return normalize(normal)
