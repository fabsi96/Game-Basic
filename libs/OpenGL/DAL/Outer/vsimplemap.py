# encoding: utf-8
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass

from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.Shader.ModelShader.modelshader import ModelShader
from OpenGL.GL import *
from libs.library import Library
import numpy as np
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL

class VSimpleMap(VOpenGL):

    def __init__(self, mapName: str, rawData: RawObject, sampleTextureFile: str):
        super(VSimpleMap, self).__init__(mapName , ModelShader(), VOpenGL.RENDER_ELEMENTS)

        """ ModelShader (all initialized ?) """

        """ Upload rawData into graphics-ram """

        self.vao = glGenVertexArrays(1)
        self.vertexVbo = self.uploadVertexData(self.vao,
                                               rawData.vertexCoords,
                                               self.sp,
                                               ModelShader.VERTICES_NAME,
                                               3)
        self.vertexCount = len(rawData.vertexCoords)
        self.indicesVbo = self.uploadIndexData(self.vao,
                                               rawData.indices)
        self.indicesCount = len(rawData.indices)
        self.textureVbo = self.uploadVertexData(self.vao,
                                                rawData.textureCoords,
                                                self.sp,
                                                ModelShader.TEXTURES_NAME,
                                                2)
        self.normalVbo = self.uploadVertexData(self.vao,
                                               rawData.normalCoords,
                                               self.sp,
                                               ModelShader.NORMALS_NAME,
                                               3)

        del rawData

        """ Textures """

        self._uploadTexture(sampleTextureFile, ModelShader.MODEL_TEXTURE_NAME, 0)

    def render(self):
        try:
            self.sp.start()
            glBindVertexArray(self.vao)

            self.sp.setMatrix4x4(ModelShader.TRANSFORMATION_MATRIX_NAME, self.getTransformationMatrix())
            self.sp.setMatrix4x4(ModelShader.PROJECTION_MATRIX_NAME, Library.mainWindow.getProjectionMatrix())
            self.sp.setMatrix4x4(ModelShader.VIEW_MATRIX_NAME, np.matrix(Library.camera.getWorldToViewMatrix()))

            if self.renderMode == VOpenGL.RENDER_ARRAYS:
                glBindBuffer(GL_ARRAY_BUFFER, self.vertexVbo)
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                for texture in self.textures:
                    glActiveTexture(GL_TEXTURE0 + texture.unit)
                    glBindTexture(GL_TEXTURE_2D, texture.vbo)
                glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

            else:
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indicesVbo)
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                for texture in self.textures:
                    glActiveTexture(GL_TEXTURE0 + texture.unit)
                    glBindTexture(GL_TEXTURE_2D, texture.vbo)
                glDrawElements(GL_TRIANGLES, self.indicesCount, GL_UNSIGNED_INT, None)

            glBindVertexArray(0)
            self.sp.stop()

        except Exception as ex:
            print(f"render: VSimpleMap [ERROR] {ex.args}")


