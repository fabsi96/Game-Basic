# encoding: utf-8
from openal import *

from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL
from libs.OpenGL.Shader.ModelShader.modelshader import ModelShader

from OpenGL.GL import *

from libs.library import Library


class VSoundBox (VOpenGL):

    DATA_SOUND_DIR = "data/sound"

    def __init__(self, rawCube: RawObject, cubeTextureFile_s: str, listener: Listener, soundFilename_s, autoRepeat=False):
        super(VSoundBox, self).__init__("Kasettenrekorder", ModelShader(), VOpenGL.RENDER_ARRAYS)

        self._filename_s = soundFilename_s
        self._listener = listener
        self._autoRepeat = autoRepeat

        try:
            """ Initialize audio """
            fullSoundPath_s = os.path.join(VSoundBox.DATA_SOUND_DIR, self._filename_s)
            if not os.path.isfile(fullSoundPath_s):
                print(f"__init__: VSoundBox [ERROR] File not found {fullSoundPath_s}")
                return

            self._source = oalOpen(fullSoundPath_s)
            alDistanceModel(AL_EXPONENT_DISTANCE_CLAMPED)
            self._source.set_reference_distance(5)
            # self._source.set_max_distance(20)
            self._source.set_rolloff_factor(1)
            self._source.set_looping(True)

            """ Initialize visible player object """
            self.vao = glGenVertexArrays(1)
            self.vertexVbo = self.uploadVertexData(self.vao,
                                                   rawCube.vertexCoords,
                                                   self.sp, ModelShader.VERTICES_NAME,
                                                   3)
            self.vertexCount = len(rawCube.vertexCoords)
            self.textureVbo = self.uploadVertexData(self.vao,
                                                    rawCube.textureCoords,
                                                    self.sp,
                                                    ModelShader.TEXTURES_NAME,
                                                    2)
            self.normalVbo = self.uploadVertexData(self.vao,
                                                   rawCube.normalCoords,
                                                   self.sp,
                                                   ModelShader.NORMALS_NAME,
                                                   3)

            del rawCube

            self._uploadTexture(cubeTextureFile_s,
                                ModelShader.MODEL_TEXTURE_NAME,
                                0)

        except Exception as ex:
            print(f"__init__: VSoundBox [ERROR] {ex.args}")

    def setAutoRepeat(self, val: bool):
        self._autoRepeat = val

    def render(self):
        try:
            """ Audio """
            self._source.set_position((self._position.x, self._position.y, self._position.z))
            if self._autoRepeat and \
                  (self._source.get_state() == AL_STOPPED or self._source.get_state() == AL_INITIAL):
                self._source.play()

            """ Graphics object """
            self.sp.start()
            self.sp.setMatrix4x4(ModelShader.TRANSFORMATION_MATRIX_NAME,
                                 self.getTransformationMatrix())
            self.sp.setMatrix4x4(ModelShader.PROJECTION_MATRIX_NAME,
                                 Library.mainWindow.getProjectionMatrix())
            self.sp.setMatrix4x4(ModelShader.VIEW_MATRIX_NAME,
                                 Library.camera.getWorldToViewMatrix())

            glBindVertexArray(self.vao)
            if self.renderMode == VOpenGL.RENDER_ARRAYS:
                glBindBuffer(GL_ARRAY_BUFFER, self.vertexVbo)
                for texture in self.textures:
                    glActiveTexture(GL_TEXTURE0 + texture.unit)
                    glBindTexture(GL_TEXTURE_2D, texture.vbo)
                    glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

            glBindVertexArray(0)
            self.sp.stop()
        except Exception as ex:
            print(f"render: VSoundBox [ERROR] {ex.args}")


    def __del__(self):
        oalQuit()