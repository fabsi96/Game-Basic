# encoding: utf-8

# libraries
from abc import abstractmethod

import numpy as np
from OpenGL.GL import *
from glm import *
from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DataLoader.Texture.texture import Texture
from libs.OpenGL.Shader.shaderprogram import ShaderProgram


# -------------------------
class VOpenGL:
    """ Summary
       Basic class of ALL OpenGL graphics objects
    """
    RENDER_NONE = "NONE"
    RENDER_ARRAYS = "ARRAYS"
    RENDER_ELEMENTS = "ELEMENTS"

    # -------------------------
    def __init__(self, objectName: str, shaderProgram: ShaderProgram, renderMode: str):
        self.name = objectName
        self.sp = shaderProgram

        self.renderMode = renderMode

        """ Single - parted - objects """
        self.vertexCount = 0
        self.indicesCount = 0
        self.vao = None
        self.vertexVbo = None
        self.textureVbo = None
        self.normalVbo = None
        self.indicesVbo = None

        # TextureData
        self.textureFiles = []
        self.textures = {}

        """ Matrices """

        # Translation
        self._position: vec3 = vec3([0.0, 0.0, 0.0])

        # Rotation
        self._xDegrees = 0
        self._yDegrees = 0
        self._zDegrees = 0

        # Scale
        self._scale: vec3 = vec3([1.0, 1.0, 1.0])

        # TransformationMatrix
        self._transformationMatrix = identity(mat4x4)

    # -------------------------
    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError("Main Class")

    """ Returns vao and vbo """

    # -------------------------
    @staticmethod
    def uploadVertexData(vao: int, data_f: list, shaderProgram: ShaderProgram, vertexShaderName: str,
                         vertsPerCoord: int) -> int:
        if vao is None or vao < 1:
            raise Exception("Vao is not defined")
        try:
            glBindVertexArray(vao)
            vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)

            numpyData = np.array(data_f, dtype=GLfloat)
            glBufferData(GL_ARRAY_BUFFER,
                         len(numpyData) * ctypes.sizeof(GLfloat),
                         numpyData,
                         GL_STATIC_DRAW)
            shaderProgram.loadVertexAttribute(vertexShaderName)
            shaderProgram.setVertexAttribute(vertexShaderName, vertsPerCoord, GL_FLOAT)

            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
            return vbo

        except Exception as ex:
            print(f"Not implemented exception. {VOpenGL.__class__} {__name__} :: {str(ex)}")

        return -1

    # -------------------------
    @staticmethod
    def uploadIndexData(vao: int, data_i: list) -> int:
        if vao is None or vao < 1:
            raise Exception("Vao is not defined.")

        try:
            glBindVertexArray(vao)
            vbo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo)
            indexData = np.array(data_i, dtype=GLuint)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indexData) * ctypes.sizeof(GLuint), indexData, GL_STATIC_DRAW)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
            return vbo

        except Exception as ex:
            print(f"Not implemented exception. {VOpenGL.__class__} {__name__} :: {str(ex)}")

    # -------------------------
    def _uploadGeometry(self, rawObject: RawObject) -> None:
        try:
            self.vao = glGenVertexArrays(1)
            if rawObject.vertexCoords.__len__() > 1:
                self.vertexVbo = VOpenGL.uploadVertexData(self.vao, rawObject.vertexCoords, self.sp, "vertexCoord", 3)
                self.vertexCount = len(rawObject.vertexCoords)
            if rawObject.indices.__len__() > 1:
                self.indicesVbo = VOpenGL.uploadIndexData(self.vao, rawObject.indices)
                self.indicesCount = len(rawObject.indices)
            if rawObject.normalCoords.__len__() > 1:
                self.normalVbo = VOpenGL.uploadVertexData(self.vao, rawObject.normalCoords, self.sp, "normalCoord", 3)
            if rawObject.textureCoords.__len__() > 1:
                self.textureVbo = VOpenGL.uploadVertexData(self.vao, rawObject.textureCoords, self.sp, "textureCoord",
                                                           2)

        except Exception as ex:
            print(f"Not implemented exception. {VOpenGL.__class__} {__name__} :: {str(ex)}")

    # -------------------------
    def _uploadTexture(self, filename, shaderTexName, unit) -> int:
        # TODO: Also suitable for 'cube maps'
        try:
            if self.sp is None:
                print(f"_uploadTexture: VOpenGL [ERROR] No ShaderProgram is configured.")
                return -1

            texture = Texture(filename, unit)
            if texture:
                self.sp.start()
                self.sp.loadTextureAttribute(shaderTexName)
                self.sp.setTextureAttribute(shaderTexName, unit)
                self.sp.stop()
                self.textures.update({texture: shaderTexName})
                return 1

        except Exception as ex:
            print(f"_uploadTexture: VOpenGL [ERROR] {ex.args}")
            return -1

    # -------------------------
    def getTransformationMatrix(self):
        self.__updateTransformationMatrix()
        return self._transformationMatrix

    # -------------------------
    def __updateTransformationMatrix(self) -> None:
        try:
            translationMatrix = translate(identity(mat4x4), self._position)

            xRotationMatrix = rotate(mat4x4(), radians(self._xDegrees), vec3(1.0, 0.0, 0.0))
            yRotationMatrix = rotate(mat4x4(), radians(self._yDegrees), vec3(0.0, 1.0, 0.0))
            zRotationMatrix = rotate(mat4x4(), radians(self._zDegrees), vec3(0.0, 0.0, 1.0))
            rotationMatrix = xRotationMatrix * yRotationMatrix * zRotationMatrix

            scaleMatrix = scale(mat4x4(), self._scale)
            self._transformationMatrix = translationMatrix * rotationMatrix * scaleMatrix

        except Exception as ex:
            print(f"[ERROR] VObject - _updateTransformationMatrix() :: {str(ex)}")

    # -------------------------
    def setPosition(self, newPos: vec3) -> None:
        self._position = newPos

    # -------------------------
    def setXRotation(self, d: float) -> None:
        self._xDegrees = d

    # -------------------------
    def setYRotation(self, d: float) -> None:
        self._yDegrees = d

    # -------------------------
    def setZRotation(self, d: float) -> None:
        self._zDegrees = d

    # ---------------------------------------
    def setScale(self, newScale: vec3) -> None:
        self._scale = newScale

    # -------------------------
    def getPosition(self) -> vec3:
        return self._position

    # -------------------------
    def getXRotation(self) -> float:
        return self._xDegrees

    # -------------------------
    def getYRotation(self) -> float:
        return self._yDegrees

    # -------------------------
    def getZRotation(self) -> float:
        return self._zDegrees

    # -------------------------
    def getScale(self) -> vec3:
        return self._scale