# encoding: utf-8
import os

import numpy as np
from OpenGL.GL import *
from PIL import Image

from core.graphics.models.ram.rawobject import RawObject
from core.graphics.models.vram.vopengl import VOpenGL
from core.graphics.shader.cubemap.cubemapshader import CubeMapShader
from core.library import Library

"""
    Documentation of the correct alignment of pictures in the cubemap

"""


# ----------------------------------------
class VCubeMap(VOpenGL):
    """ Summary
       Generates a cube map with a
       * basic box (cube)
       * six ordered textures for correct translation into shader
    """
    # TODO: Loaded in RawObject
    SIZE = 100
    VERTICES = [
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

    # ----------------------------------------
    def __init__(self, rawCube: RawObject, cubeMapType="sky"):
        try:
            # Correct order! Right - Left - Top - Bottom - Back - Front
            super(VCubeMap, self).__init__("SkyMap", CubeMapShader(), VOpenGL.RENDER_ARRAYS)

            self.vao = glGenVertexArrays(1)
            self.vertexVbo = self.uploadVertexData(self.vao,
                                                   rawCube.vertexCoords,
                                                   self.sp,
                                                   CubeMapShader.VERTICES_NAME,
                                                   3)
            self.vertexCount = len(rawCube.vertexCoords)

            self.cubeTexID = -1
            self.textureFiles = []
            fileType_s = "png"
            self.textureFiles.append("right." + fileType_s)
            self.textureFiles.append("left." + fileType_s)
            self.textureFiles.append("top." + fileType_s)
            self.textureFiles.append("bottom." + fileType_s)
            self.textureFiles.append("back." + fileType_s)
            self.textureFiles.append("front." + fileType_s)

            self.__uploadCubeMap(cubeMapType, self.textureFiles)

        except Exception as ex:
            print(str(ex))

    # ----------------------------------------
    def __uploadCubeMap(self, cubeMapFolder: str, filesOrder: list) -> None:
        try:
            # Upload cubemap textures
            self.sp.start()
            self.cubeTexID = glGenTextures(1)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubeTexID)
            for i in range(0, 6):
                fullPath = os.path.join("data/res", cubeMapFolder, filesOrder[i])
                image: Image = Image.open(fullPath)
                # img = pygame.image.load(fullPath).convert_alpha()

                image_rgba = image.convert("RGBA")
                # image_rgb = image.convert("RGB")

                img_rgba_data = np.array(image_rgba.getdata())

                # img_rgb_data = np.array(image_rgb.getdata())
                glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                             0,
                             GL_RGBA,
                             image_rgba.width,
                             image_rgba.height,
                             0,
                             GL_RGBA,
                             GL_UNSIGNED_BYTE,
                             img_rgba_data)

            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

            self.sp.stop()

        except Exception as ex:
            print(f"__uploadCubeMap - CubeMap Error {ex.args}")

        """
                        from datetime import datetime
                beforeLoading_o = datetime.now()
                afterLoading_o = datetime.now()
                loadingTime_o = afterLoading_o - beforeLoading_o
                loadingTime_seoncds = loadingTime_o.total_seconds()
                print(f"[DEBUG] ('{fullPath}' Mb / '{loadingTime_seoncds}' sec) ")

        """

    # ----------------------------------------
    def render(self) -> None:
        try:
            self.sp.start()
            glBindVertexArray(self.vao)
            if self.renderMode == VOpenGL.RENDER_ARRAYS:
                glBindBuffer(GL_ARRAY_BUFFER, self.vertexVbo)

                self.sp.setMatrix4x4(CubeMapShader.PROJECTION_MATRIX_NAME,
                                     Library.mainWindow.getProjectionMatrix())
                self.sp.setMatrix4x4(CubeMapShader.VIEW_MATRIX_NAME,
                                     Library.camera.getWorldToViewMatrix())
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubeTexID)
                glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)
            else:
                print(f"render: VCubeMap [ERROR] Render Mode not found !")

            glBindVertexArray(0)
            self.sp.stop()

        except Exception as ex:
            print(f"render: VCubeMap [ERROR] {ex.args}")
