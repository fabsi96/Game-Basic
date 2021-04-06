# encoding: utf-8
import numpy as np
from OpenGL.GL import *

from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL
from libs.OpenGL.Shader.ModelShader.modelshader import ModelShader
from libs.OpenGL.Shader.shaderprogram import ShaderProgram
from libs.library import Library


class VBlenderParts(VOpenGL):

    def __init__(self, rawObject: RawObject, sp: ShaderProgram):
        super(VBlenderParts, self).__init__(rawObject, sp)
        self.sp = sp
        self.textureFiles = rawObject.textureFiles
        self.vaos = []
        self.verticesVbos = []
        self.verticesCount = []
        self.normalsVbos = []
        self.texturesVbos = []
        self.textures = {}
        self.indicesVbos = []
        self.indicesCount = []

        # Load data into graphics memory
        self.initializeRawObject(rawObject)

    def initializeRawObject(self, rawObject: RawObject):
        try:
            for i in range(0, len(rawObject.verticesMeshes)):
                currentVertices = rawObject.verticesMeshes[i]
                currentNormals = rawObject.normalsMeshes[i]
                currentTextures = rawObject.texturesMeshes[i]
                currentIndices = rawObject.indicesMeshes[i]

                vao = glGenVertexArrays(1)
                self.vaos.append(vao)
                currentVerticesVbo = VOpenGL.uploadVertexData(vao, currentVertices, self.sp, "vertexCoord", 3)
                self.verticesCount.append(int(len(currentVertices)))
                self.verticesVbos.append(currentVerticesVbo)
                currentNormalsVbo = VOpenGL.uploadVertexData(vao, currentNormals, self.sp, "normalCoord", 3)
                self.normalsVbos.append(currentNormalsVbo)
                currentTexturesVbo = VOpenGL.uploadVertexData(vao, currentTextures, self.sp, "textureCoord", 2)
                self.texturesVbos.append(currentTexturesVbo)
                currentIndicesVbo = VOpenGL.uploadIndexData(vao, currentIndices)
                self.indicesVbos.append(currentIndicesVbo)
                self.indicesCount.append(int(len(currentIndices)))

            textureUnitRunner = 0
            for textureFile in rawObject.textureFiles:
                self._uploadTexture(textureFile, ModelShader.DEFAULT_TEXTURE_NAME, textureUnitRunner)
                textureUnitRunner += 1

        except Exception as ex:
            print(f"__init__: VBlenderParts [ERROR] {ex.args}")

    def render(self):
        try:
            for i in range(0, len(self.vaos)):
                vao = self.vaos[i]
                verticesVbo = self.verticesVbos[i]
                currentVerticesCount = self.verticesCount[i]
                indicesVbo = self.indicesVbos[i]
                currentIndicesCount = self.indicesCount[i]

                self.sp.start()
                glBindVertexArray(vao)
                glBindBuffer(GL_ARRAY_BUFFER, verticesVbo)

                self._updateTransformationMatrix()
                self.sp.setMatrix4x4("transformMatrix", self._transformationMatrix)
                self.sp.setMatrix4x4("projectionMatrix", Library.mainWindow.getProjectionMatrix())
                self.sp.setMatrix4x4("viewMatrix", np.matrix(Library.camera.getWorldToViewMatrix()))

                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                if self.renderMode == "ELEMENTS":
                    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indicesVbo)
                    for texture in self.textures:
                        glActiveTexture(GL_TEXTURE0 + texture.unit)
                        glBindTexture(GL_TEXTURE_2D, texture.vbo)
                    glDrawElements(GL_TRIANGLES, currentIndicesCount, GL_UNSIGNED_INT, None)
                elif self.renderMode == "ARRAYS":
                    for texture in self.textures:
                        glActiveTexture(GL_TEXTURE0 + texture.unit)
                        glBindTexture(GL_TEXTURE_2D, texture.vbo)

                    glDrawArrays(GL_TRIANGLES, 0, currentVerticesCount)

                glBindVertexArray(0)
                self.sp.stop()


        except Exception as ex:
            print(f"render: VBlenderParts [ERROR] {ex.args}")
