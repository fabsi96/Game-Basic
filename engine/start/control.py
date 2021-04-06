# encodig: utf-8

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from libs.Qt.vglwidget import VGLWidget
    from libs.OpenGL.DataLoader.dataloader import DataLoader

    from libs.OpenGL.DAL.Outer.vsimpledae import VSimpleDae
    from libs.OpenGL.DAL.Outer.vsimplemap import VSimpleMap

from glm import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from engine.control import VControl
from libs.OpenGL.camera import Camera
from libs.library import Library


# Local


class StartControl(VControl):
    """ Summary
       Self defined control-class which implements elementary operations

       * Interface between User and BackEnd functions
    """
    MOUSE_SPEED_OBJECT = 1.0
    MOUSE_SPEED_FREE_FLIGHT = 0.01
    MIN_PITCH = 90
    MAX_PITCH = 270
    MIN_YAW = -170
    MAX_YAW = +170

    TEST = "test"

    # -----------------
    def __init__(self, loader, window):
        super(StartControl, self).__init__()
        self.loader: DataLoader = loader
        self.window: VGLWidget = window

        try:
            self.models = []

            # Init (possible) user inputs
            self.window.setKeyPressCallback(self.keyPressCallback)
            self.window.setMousePressCallback(self.mousePressCallback)
            self.window.setMousePressCallback(self.mousePressCallback)
            self.window.setMouseReleaseCallback(self.mouseReleaseCallback)
            self.window.setMouseMoveCallback(self.mouseMoveCallback)
            self.window.setMouseWheelCallback(self.mouseWheelCallback)

            self.ground: VSimpleMap = self.loader.getSimpleMap("My Map", 100, 2, "grass.jpg")
            self.window.addVObject(self.ground)

            self.cube: VSimpleDae = self.loader.getSimpleDaeObject("Quad",
                                                                   "TestQuad/testQuad.dae",
                                                                   "path.jpg")
            self.cube.setPosition(vec3(12.0, 0.0, 12.0))
            self.cube.setScale(vec3(1.6, 1.6, 1.6))
            self.window.addVObject(self.cube)

            self.cubeMap = self.loader.getVCubeMap(100, "sky")
            self.window.addVObject(self.cubeMap)

            self.soundBox = self.loader.getSoundBox("kygo.wav")
            self.soundBox.setPosition(vec3(50.0, 1.0, 50.0))
            self.soundBox.setScale(vec3(0.7,0.7, 0.7))
            self.window.addVObject(self.soundBox)

            self.window.xAttenuationSlider.valueChanged.connect(self.attenueChanged)
            self.window.yAttenuationSlider.valueChanged.connect(self.attenueChanged)
            self.window.zAttenuationSlider.valueChanged.connect(self.attenueChanged)

        except Exception as ex:
            print(f"__init__: StartControl [ERROR] {ex.args}")

        self.mouseLeftPressed = False
        self.lastMouseXPos = 0
        self.lastMouseYPos = 0

    # -----------------
    def attenueChanged(self):
        xVal = self.window.xAttenuationSlider.value() / 1000.0
        yVal = self.window.yAttenuationSlider.value() / 1000.0
        zVal = self.window.zAttenuationSlider.value() / 1000.0
        # self.lightSource.setAttenuation(vec3(xVal, yVal, zVal))

    # -----------------
    def onEvent(self, event: QEvent) -> None:
        """
            Process all events here and divide them to mouse and key events -> functions
        :param event:
        :return:
        """
        pass

    # ------------------
    def keyPressCallback(self, keyCode: int):
        # TODO: Threaded user inputs (two or more at the same time)
        try:
            if keyCode == Qt.Key_A:
                """ Moving camera left """
                Library.camera.strafeLeft()

            elif keyCode == Qt.Key_D:
                """ Moving camera right """
                Library.camera.strafeRight()

            elif keyCode == Qt.Key_W:
                """ Moving camera forward """
                Library.camera.moveForward()

            elif keyCode == Qt.Key_S:
                """ Moving camera backward """
                Library.camera.moveBackward()

            elif keyCode == Qt.Key_R:
                """ Increase cams height """
                Library.camera._pitch = 0.0
                Library.camera._yaw = 0.0
                Library.camera.moveUp()

            elif keyCode == Qt.Key_F:
                """ Decreases cams height """
                Library.camera.moveDown()

            elif keyCode == Qt.Key_Escape:
                Library.app.exit(0)

            elif keyCode == Qt.Key_X:
                pass

            elif keyCode == Qt.Key_Y:
                pass

            elif keyCode == Qt.Key_Z:
                pass
            elif keyCode == Qt.Key_Shift:
                pass
            else:
                print(f"keyPressCallback: StartControl [DEBUG] Key not found {keyCode}")

            # distanceToSound = length(self.soundBox.getPosition() - Library.camera.getPosition())
            # print(f"[DISTANCE] {distanceToSound}")

        except Exception as ex:
            print(f"keyPressCallback: StartControl [ERROR] {ex.args}")

    # ------------------
    def mousePressCallback(self, mouseEvent: QMouseEvent) -> None:
        try:
            if mouseEvent.button() == Qt.LeftButton:
                self.mouseLeftPressed = True

        except Exception as ex:
            print(f"mousePressCallback: StartControl [ERROR] {ex.args}")

    # ------------------
    def mouseReleaseCallback(self, mouseEvent: QMouseEvent) -> None:
        try:
            if mouseEvent.button() == Qt.LeftButton:
                self.mouseLeftPressed = False

        except Exception as ex:
            print(f"mouseReleaseCallback: StartControl [ERROR] {ex.args}")

    # ------------------
    def mouseMoveCallback(self, mouseEvent: QMouseEvent) -> None:
        deltaX = mouseEvent.x() - self.lastMouseXPos
        deltaY = mouseEvent.y() - self.lastMouseYPos
        try:
            deltaVector = vec2(deltaX, deltaY)
            deltaLength = length(deltaVector)
            self.lastMouseXPos = mouseEvent.x()
            self.lastMouseYPos = mouseEvent.y()
            if deltaLength > 25:
                return
            if self.mouseLeftPressed:
                """ Free camera - turning around """
                viewDirection = Library.camera.getViewDirection()
                toRotateAround = cross(viewDirection, Library.camera.getUpVector())
                rotator = rotate(identity(mat4x4), deltaX * -self.MOUSE_SPEED_FREE_FLIGHT,
                                 Library.camera.getUpVector()) * \
                          rotate(identity(mat4x4), deltaY * -self.MOUSE_SPEED_FREE_FLIGHT, toRotateAround)

                viewDirection = mat3x3(rotator) * viewDirection
                Library.camera.setViewDirection(viewDirection)

        except Exception as ex:
            print(f"mouseMoveCallback: StartControl [ERROR] {ex.args}")

        # Static - must be updated every time
        self.lastMouseXPos = mouseEvent.x()
        self.lastMouseYPos = mouseEvent.y()

    # ------------------
    def mouseWheelCallback(self, wheelEvent: QWheelEvent) -> None:
        try:
            """ Inc/Dec distance from object """
            if wheelEvent.angleDelta().y() > 0:
                Camera.DISTANCE_TO_TARGET -= 0.8
            else:
                Camera.DISTANCE_TO_TARGET += 0.8

        except Exception as ex:
            print(f"mouseWheelCallback: StartControl [ERROR] {ex.args}")
