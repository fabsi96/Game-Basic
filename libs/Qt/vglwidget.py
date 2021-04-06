# encoding: utf-8

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from libs.OpenGL.DAL.Outer.vopengl import VOpenGL

import os
import re
from glm import *

from OpenGL.GL import *
from PyQt5.QtCore import QTimerEvent, QRect, QPoint, Qt
from PyQt5.QtGui import QMouseEvent, QShowEvent, QWheelEvent, QKeyEvent
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtWidgets import *

from engine.start.view import StartView
from libs.library import Library
from settings import Settings
from datetime import datetime

class VGLWidget(QOpenGLWidget):
    """ Summary

    """
    ShaderVersion = -1  # 440 auf Laptop(s)

    # --------------------------
    def __init__(self, width:int , height: int):
        super(VGLWidget, self).__init__()
        Library.beforeStart_o = datetime.now()

        """ Graphics context """
        self.makeCurrent()
        self.objects = []

        """ OpenGL Information """
        # glInformation = VGLWidget.getOpenglInfo()
        # print("OpenGL INFO :: \n {0}".format(glInformation))
        VGLWidget.ShaderVersion = int(460)

        """ Important Window (SETTINGS) stuff """

        self.setGeometry(0, 20, width, height)
        self.timerId = self.startTimer(10)

        # User inputs
        self.keyPressCallbackFunc = None
        self.keyReleaseCallbackFunc = None
        self.mousePressCallbackFunc = None
        self.mouseReleaseCallbackFunc = None
        self.mouseMoveCallbackFunc = None
        self.mouseWheelCallbackFunc = None
        self.keysPressed_d = {}
        self.mousePressed_d = {}

        # Projection matrix. Measured from window size and camera attributes
        self._projectionMatrix = None

        self.initUI()

    def initUI(self):
        try:
            layout = QVBoxLayout()

            self.xAttenuationSlider = QSlider(Qt.Horizontal, parent=self)
            self.xAttenuationSlider.setGeometry(0, 0, 400, 20)
            self.xAttenuationSlider.setTickInterval(1)
            self.xAttenuationSlider.setMinimum(1)
            self.xAttenuationSlider.setMaximum(1000)
            self.yAttenuationSlider = QSlider(Qt.Horizontal, parent=self)
            self.yAttenuationSlider.setGeometry(0, 20, 400, 20)
            self.yAttenuationSlider.setTickInterval(1)
            self.yAttenuationSlider.setMinimum(1)
            self.yAttenuationSlider.setMaximum(1000)
            self.zAttenuationSlider = QSlider(Qt.Horizontal, parent=self)
            self.zAttenuationSlider.setGeometry(0, 40, 400, 20)
            self.zAttenuationSlider.setTickInterval(1)
            self.zAttenuationSlider.setMinimum(1)
            self.zAttenuationSlider.setMaximum(1000)

        except Exception as ex:
            print(f"initUI: VGLWidget [ERROR] {ex.args}")

    # --------------------------
    def timerEvent(self, a0: QTimerEvent):
        self.repaint()

    def showEvent(self, showEvent: QShowEvent):
        try:
            # read file
            workingDir_s = os.getcwd()
            start_scr: str = Settings.gameSettings["scriptstart"]["path"]
            fullExecPath = os.path.join(workingDir_s, Settings.engineDir, start_scr, "view" + ".py")

            # Execute first scripts
            start = StartView(Library.loader, Library.mainWindow)

            # StartModule = getattr(sys.modules[__name__], start_scr)
            # if StartModule:
            #     start = StartModule(Library.loader, Library.mainWindow)  # StartView(Library.loader, Library.mainWindow)
            # if os.path.isfile(fullExecPath):
            #     exec(open(fullExecPath).read(), globals())
            # pass

            if Library.afterStart_o is None:
                Library.afterStart_o = datetime.now()
                startElapsedTime_o = Library.afterStart_o - Library.beforeStart_o
                print(f"[DEBUG] FULL Elapsed time: '{startElapsedTime_o.total_seconds()}' secs")

        except Exception as ex:
            print("Exception :: {0}".format(str(ex)))

    # --------------------------
    def getProjectionMatrix(self) -> mat4x4:
        self._projectionMatrix = perspective(120.0, self.width() / self.height(), 0.1, 1000.0)
        return self._projectionMatrix

    """ Event callbacks"""

    # --------------------------
    def setKeyPressCallback(self, callbackFunc) -> None:
        self.keyPressCallbackFunc = callbackFunc

    # --------------------------
    def setKeyReleaseCallback(self, callbackFunc) -> None:
        self.keyReleaseCallbackFunc = callbackFunc

    # --------------------------
    def setMousePressCallback(self, callbackFunc) -> None:
        self.mousePressCallbackFunc = callbackFunc

    # --------------------------
    def setMouseReleaseCallback(self, callbackFunc) -> None:
        self.mouseReleaseCallbackFunc = callbackFunc

    # --------------------------
    def setMouseMoveCallback(self, callbackFunc) -> None:
        self.mouseMoveCallbackFunc = callbackFunc

    # --------------------------
    def setMouseWheelCallback(self, callbackFunc) -> None:
        self.mouseWheelCallbackFunc = callbackFunc

    # --------------------------
    def keyPressEvent(self, keyEvent: QKeyEvent) -> None:
        try:
            self.keysPressed_d.update({keyEvent.key().__str__(): keyEvent.key()})

        except Exception as ex:
            print(f"keyPressEvent: MyGLWindow [ERROR] {ex.args}")

    # --------------------------
    def keyReleaseEvent(self, keyEvent: QKeyEvent) -> None:
        try:
            del self.keysPressed_d[keyEvent.key().__str__()]

        except Exception as ex:
            print(f"keyReleaseEvent: MyGLWindow [ERROR] {ex.args}")

    # --------------------------
    def mousePressEvent(self, mouseEvent: QMouseEvent) -> None:
        if self.mousePressCallbackFunc:
            self.mousePressCallbackFunc(mouseEvent)

    # --------------------------
    def mouseMoveEvent(self, mouseEvent: QMouseEvent) -> None:
        if self.mouseMoveCallbackFunc:
            self.mouseMoveCallbackFunc(mouseEvent)

        self.mousePressed_d.update({mouseEvent.button().__str__(): mouseEvent})

    # --------------------------
    def mouseReleaseEvent(self, mouseEvent: QMouseEvent) -> None:
        if self.mouseReleaseCallbackFunc:
            self.mouseReleaseCallbackFunc(mouseEvent)

    # --------------------------
    def wheelEvent(self, wheelEvent: QWheelEvent) -> None:
        if self.mouseWheelCallbackFunc:
            self.mouseWheelCallbackFunc(wheelEvent)

    # --------------------------
    def addVObject(self, obj: VOpenGL) -> None:
        if obj:
            self.objects.append(obj)

    # --------------------------
    def initializeGL(self) -> None:
        try:
            glClearColor(0.0, 0.0, 0.0, 1.0)
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_TEXTURE_2D)
            # CLOCKWISE
            # glEnable(GL_CULL_FACE)
            # glEnable(GL_TEXTURE_CUBE_MAP)
            QApplication.setKeyboardInputInterval(1)

        except Exception as ex:
            print("initializeGL() - Exception :: {0}".format(str(ex)))

    # --------------------------
    def paintGL(self) -> None:
        try:
            """ Keyboard inputs """
            if self.keyPressCallbackFunc and self.keysPressed_d:
                for key_o in self.keysPressed_d:
                    self.keyPressCallbackFunc(self.keysPressed_d[key_o])

            """ Rendering """
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            Library.camera.update()
            for obj in self.objects:
                obj.render()

            """
            if Library.vMap is not None:
                Library.vMap.render()
            """

        except Exception as ex:
            print(f"paintGL: VGLWidget [ERROR] {ex.args}")

    # --------------------------
    def resizeGL(self, width, height) -> None:
        glViewport(0, 0, width, height)

    # --------------------------
    @staticmethod
    def getOpenglInfo() -> str:
        try:
            info = """
               Vendor: {0}
               Renderer: {1}
               OpenGL Version: {2}
               Shader Version: {3}
           """.format(
                  glGetString(GL_VENDOR),
                  glGetString(GL_RENDERER),
                  glGetString(GL_VERSION),
                  glGetString(GL_SHADING_LANGUAGE_VERSION))
            versionStr: str = glGetString(GL_SHADING_LANGUAGE_VERSION).decode('ascii')
            versionStr = re.sub("\D", "", versionStr)  # \D -> (D)igits
            print("Version string :: {}".format(versionStr))
            VGLWidget.ShaderVersion = int(versionStr)
            return info

        except Exception as ex:
            print(f"getOpenglInfo: MyGLWindow [ERROR] {ex.args}")
            return "Could not extract shading information"
