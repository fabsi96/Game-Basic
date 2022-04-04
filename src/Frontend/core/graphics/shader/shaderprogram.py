# encoding: utf-8

try:
    import weakref

    from OpenGL.GL import *
    import numpy as np
    from glm import *

except Exception as e:
    print(f"Import exception {str(e)}")


# -----------------------------------------------
class ShaderProgram:
    """ Summary
       DOC:
 
       shaderprogram with its files, attribs names and ids, program/shader ids,
 
       - implement files
       - implement error handling
    """
    SHADER_DIR = "core//graphics/shader/"
    __refs__ = []

    positionName = "vertexCoord"
    colorName = "colorCoord"
    texturesName = "textureCoord"

    grayScaleTextureName = "grayScaleTexture"
    grassTextureName = "grassTexture"
    sandTextureName = "sandTexture"

    # Matrices
    modelMatrixName = "modelMatrix"
    projectionMatrixName = "projectionMatrix"
    viewMatrixName = "viewMatrix"

    # Light
    # Ambient
    AMBIENT_NAME = "ambientLight"
    DEFAULT_AMBIENT_LIGHT = vec3(0.6, 0.6, 0.6)

    # Diffuse
    DIFFUSE_NAME = "lightPosition"

    # Specular
    SPECULAR_NAME = ""

    # Array of objects (VLightSource)
    POINT_LIGHTS = []

    # -----------------------------------------------
    def __init__(self, shaderName: str, progID: int):
        # Keep track of all class references
        self.__class__.__refs__.append(weakref.proxy(self))

        # Basic attributes
        self.__name = shaderName
        self.__programID = progID

        self.__attrIds = {}
        self.__matrixIds = {}
        self.__intIds = {}
        self.__floatIds = {}
        self.__texAttrIds = {}
        self.__vec3Ids = {}
        # -----------------------------------------------

        # Ambient light (basic groundcolor)
        # Will be set in EACH shader, that exist!
        self._ambientLightColor = ShaderProgram.DEFAULT_AMBIENT_LIGHT
        self._ambientLightShaderName = "ambientLight"
        self.setAmbientLight()

        # Diffuse Light

        # TODO
        # Specular Light

    # -----------------------------------------------
    def getProgramID(self) -> int:
        return self.__programID

    # -----------------------------------------------
    def getAmbientLightColor(self):
        return self._ambientLightColor

    # -----------------------------------------------
    def setAmbientLightColor(self, val: vec3):
        self._ambientLightColor = val
        self.setAmbientLight()

    # -----------------------------------------------
    def start(self) -> None:
        if self.__programID is None or self.__programID == -1:
            raise Exception("start: ShaderProgram [ERROR] shader program could not start. Check your shader sources.")
        else:
            glUseProgram(self.__programID)

    # -----------------------------------------------
    def stop(self) -> None:
        glUseProgram(0)

    # -----------------------------------------------
    def loadVertexAttribute(self, attrName: str) -> None:
        try:
            if self.__programID is not None and self.__programID != -1:
                index = glGetAttribLocation(self.__programID, attrName)
                if index == -1:
                    print(
                        f"loadVertexAttribute: ShaderProgram [WARNING] Vertex-attribute '{attrName}' in shader '{self.__name}' not found.")
                else:
                    self.__attrIds.update({attrName: index})

        except Exception as ex:
            print(f"loadVertexAttribute: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    def setVertexAttribute(self,
                           attrName: str,
                           numVerts: int,
                           vertType) -> None:
        try:
            index = self.__attrIds.get(attrName)
            if index is None or index == -1:
                print(
                    f"setVertexAttribute: ShaderProgram [WARNING] Vertex-attribute '{attrName}' in shader '{self.__name}' not found.")

            else:
                glEnableVertexAttribArray(index)
                glVertexAttribPointer(index, numVerts, vertType, GL_FALSE, 0, None)

        except Exception as ex:
            print(f"setVertexAttribute: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    def loadMatrix4x4(self, matrixName: str) -> None:
        try:
            if self.__programID is not None and self.__programID != -1:
                index = glGetUniformLocation(self.__programID, matrixName)
                if index == -1:
                    print(
                        f"loadMatrix4x4: ShaderProgram [WARNING]  Matrix '{matrixName}' in shader '{self.__name}' not found.")
                else:
                    self.__matrixIds.update({matrixName: index})

        except Exception as ex:
            print(f"loadMatrix4x4: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    def setMatrix4x4(self, matrixName: str, matrix: tmat4x4) -> None:
        try:
            index = self.__matrixIds.get(matrixName)
            if index is None:
                print(
                    f"setMatrix4x4: ShaderProgram [WARNING] Matrix '{matrixName}' in shader '{self.__name}' not found.")
            else:
                glUniformMatrix4fv(index, 1, GL_FALSE, np.matrix(matrix, dtype=GLfloat))

        except Exception as ex:
            print(f"setMatrix4x4: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    def loadIntAttribute(self, attrName: str) -> None:
        try:
            if self.__programID is not None and self.__programID != -1:
                index = glGetUniformLocation(self.__programID, attrName)
                if index == -1:
                    print(
                        f"loadIntAttribute: ShaderProgram [WARNING] Integer attribute '{attrName}' in shader '{self.__name}' not found.")
                else:
                    self.__attrIds.update({attrName: index})

        except Exception as ex:
            print(f"loadIntAttribute: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    def setIntAttribute(self, attrName: str, value: int) -> None:
        try:
            index = self.__attrIds.get(attrName)
            if index is None or index == -1:
                print(
                    f"setIntAttribute: ShaderProgram [WARNING]  Integer attribute '{attrName}' in shader '{self.__name}' not found.")
            else:
                glUniform1i(index, np.int(value))

        except Exception as ex:
            print(f"setIntAttribute: ShaderProgram [ERROR]  {ex.args}")

    # -----------------------------------------------
    def loadFloatAttribute(self, attrName: str) -> None:
        try:
            if self.__programID is not None and self.__programID != -1:
                index = glGetAttribLocation(self.__programID, attrName)
                if index == -1:
                    print(f"[ERROR] Float attribute '{attrName}' in shader '{self.__name}' not found.")
                else:
                    self.__attrIds.update({attrName: index})

        except Exception as ex:
            print(f"loadFloatAttribute: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    def setFloatAttribute(self, attrName: str, value: float) -> None:
        try:
            index = self.__attrIds.get(attrName)
            if index is None or index == -1:
                print(
                    f"setFloatAttribute: ShaderProgram [WARNING] Float attribute '{attrName}' in shader '{self.__name}' not found.")
            else:
                glUniform1f(index, value)

        except Exception as ex:
            print(f"setFloatAttribute: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    def loadTextureAttribute(self, attrName: str) -> None:
        try:
            if self.__programID and self.__programID != -1:
                index = glGetUniformLocation(self.__programID, attrName)
                if index == -1:
                    print(
                        f"loadTextureAttribute: ShaderProgram [WARNING] Texture '{attrName}' in shader '{self.__name}' not found.")
                else:
                    self.__texAttrIds.update({attrName: index})

        except Exception as ex:
            print(f"loadTextureAttribute: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    def setTextureAttribute(self, attrName: str, value: int) -> None:
        try:
            index = self.__texAttrIds.get(attrName)
            if index is None or index == -1:
                print(
                    f"setTextureAttribute: ShaderProgram  [WARNING] Texture '{attrName}' in shader '{self.__name}' not found.")
            else:
                glUniform1i(index, value)

        except Exception as ex:
            print(f"setTextureAttribute: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    def loadVector3f(self, attrName: str) -> None:
        try:
            if self.__programID and self.__programID != -1:
                index = glGetUniformLocation(self.__programID, attrName)
                if index == -1:
                    print(
                        f"loadVector3f: ShaderProgram [WARNING] Uniform '{attrName}' in shader '{self.__name}' not found.")
                else:
                    self.__vec3Ids.update({attrName: index})

        except Exception as ex:
            print(f"loadVector3f: ShaderProgram [ERROR] {ex.args} ")

    # -----------------------------------------------
    def setVector3f(self, attrName: str, value: vec3) -> None:
        try:
            index = self.__vec3Ids.get(attrName)
            if index is None or index == -1:
                print(f"setVector3f: ShaderProgram [WARNING] Uniform '{attrName}' in shader '{self.__name}' not found.")
            else:
                glUniform3fv(index, 1, np.array(value, dtype=GLfloat))
        except Exception as ex:
            print(f"setVector3f: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    @staticmethod
    def setAmbientLight() -> None:
        """ Ambient light """
        try:
            for ref in ShaderProgram.__refs__:
                ref: ShaderProgram

                ref.start()
                ref.loadVector3f(ShaderProgram.AMBIENT_NAME)
                ref.setVector3f(ShaderProgram.AMBIENT_NAME, ref.getAmbientLightColor())
                ref.stop()

        except Exception as ex:
            print(f"setAmbientLight: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    @staticmethod
    def setAmbientLightColor(color: vec3) -> None:
        try:
            for ref in ShaderProgram.__refs__:
                ref: ShaderProgram
                ref.setAmbientLightColor(color)

        except Exception as ex:
            print(f"setAmbientLightColor: ShaderProgram [ERROR] {ex.args}")

    # -----------------------------------------------
    @staticmethod
    def addLightSource(src) -> None:
        ShaderProgram.POINT_LIGHTS.append(src)  # VLightSource
        ShaderProgram.updateLightSources()

    # -----------------------------------------------
    @staticmethod
    def updateLightSources() -> None:
        try:

            pointLightPosArr = []
            pointLightAttenuationArr = []
            # Set up array for shader program
            for src in ShaderProgram.POINT_LIGHTS:
                pointLightPosArr.append(np.array(src.getPosition()))
                pointLightAttenuationArr.append(np.array(src.getAttenuation()))

            for ref in ShaderProgram.__refs__:
                ref: ShaderProgram

                ref.start()
                pLightsPositionShaderName = "pointLightsPosition"
                pLightsAttenuationShaderName = "pointLightsAttenuation"

                pLightsPositionLoc = glGetUniformLocation(ref.__programID,
                                                          pLightsPositionShaderName)
                if pLightsPositionLoc > -1:
                    glUniform3fv(pLightsPositionLoc,
                                 pointLightPosArr.__len__(),
                                 np.array(pointLightPosArr))
                else:
                    print(
                        f"updateLightSource: ShaderProgram [WARNING] Uniform '{pLightsPositionShaderName}' in shader '{ref.__name}' not found.")

                pLightsAttenuationLoc = glGetUniformLocation(ref.__programID,
                                                             pLightsAttenuationShaderName)
                if pLightsAttenuationLoc > -1:
                    glUniform3fv(pLightsAttenuationLoc,
                                 pointLightAttenuationArr.__len__(),
                                 np.array(pointLightAttenuationArr))
                else:
                    print(
                        f"updateLightSource: ShaderProgram [WARNING] Uniform '{pLightsAttenuationShaderName}' in shader '{ref.__name}' not found.")

                ref.stop()

        except Exception as ex:
            print(f"updateLightSources: ShaderProgram [ERROR] {ex.args}")

    """
    def setSpecularLight(self):
       try:
          self.start()
          self.loadVector3f("cameraPosition")
          self.setVector3f("cameraPosition", np.array(Library.camera.getPosition(), dtype=GLfloat))
          self.stop()
 
       except Exception as ex:
          raise ex
 
    def updateSpecularLight(self):
       try:
          if Library.camera is not None:
             self.loadVector3f("cameraPosition")
             self.setVector3f("cameraPosition", np.array(Library.camera.getPosition(), dtype=GLfloat))
 
       except Exception as ex:
          raise ex
    """
