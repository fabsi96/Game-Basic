# encoding: utf-8
from glm import *


# -------------------------------
from openal import oalGetListener, Listener

from libs.OpenGL.DAL.Outer.vopengl import VOpenGL


class Camera:
    """ Summary

    """
    MOVEMENT_SPEED = .25
    DISTANCE_TO_TARGET = 3

    # -------------------------------
    def __init__(self, target: VOpenGL = None):
        self._position = vec3([0.0, 5.0, 0.0])
        self._viewDirection = vec3([0.66, -0.25, 0.706])
        self._upVector = vec3([0.0, 1.0, 0.0])

        self._targetUnit = target
        # Vertical additional
        self._pitch = 90
        # Horizontal additional
        self._yaw = 0.0
        self._increaseMovement = False

        # Sound listener
        self._listener: Listener = oalGetListener()

    # -------------------------------
    def followUnit(self, target: VOpenGL) -> None:
        self._targetUnit = target

    """ Follow object calculations """

    # -------------------------------
    def update(self) -> None:
        try:
            """ A u d i o """
            self._listener.set_position((self._position.x, self._position.y, self._position.z))
            self._listener.set_orientation((self._viewDirection.x, self._viewDirection.y, self._viewDirection.z,
                                            self._upVector.x, self._upVector.y, self._upVector.z))

            """ Follow a target """
            if self._targetUnit is not None:
                self._targetUnit: VOpenGL
                targetYRotation = self._targetUnit.getZRotation()
                tPos = self._targetUnit.getPosition()
                newXPosition = tPos.x - Camera.DISTANCE_TO_TARGET * sin(radians(targetYRotation + self._yaw))
                newYPosition = tPos.y + Camera.DISTANCE_TO_TARGET * sin(radians(self._pitch))
                newZPosition = tPos.z - Camera.DISTANCE_TO_TARGET * cos(radians(targetYRotation + self._yaw))

                self._position = vec3([newXPosition, newYPosition, newZPosition])
                self._viewDirection = tPos - self._position
            else:
                pass

        except Exception as ex:
            print(f"Not implemented exception. {self.__class__} {__name__} :: {str(ex)}")

    """ Getter """

    # -------------------------------
    def getPosition(self) -> vec3:
        return self._position

    # -------------------------------
    def getViewDirection(self) -> vec3:
        return self._viewDirection

    # -------------------------------
    def getUpVector(self) -> vec3:
        return self._upVector

    """ Setter """

    # -------------------------------
    def setPosition(self, newPos: vec3) -> None:
        self._position = newPos
        self.update()

    # -------------------------------
    def setViewDirection(self, newViewDirection: vec3) -> None:
        self._viewDirection = newViewDirection
        self.update()

    # -------------------------------
    def setUpVector(self, newUpVector: vec3) -> None:
        self._upVector = newUpVector
        self.update()

    """ For following objects """

    # -------------------------------
    def getPitch(self) -> float:
        return self._pitch

    # -------------------------------
    def getYaw(self) -> float:
        return self._yaw

    # -------------------------------
    def setPitch(self, value: float) -> None:
        self._pitch = value
        self.update()

    # -------------------------------
    def setYaw(self, value: float) -> None:
        self._yaw = value
        self.update()

    """ View matrix for shaders """

    # -------------------------------
    def getWorldToViewMatrix(self) -> mat4x4:
        return lookAt(self._position, self._position + self._viewDirection, self._upVector)

    """ Camera movement """

    # -------------------------------
    def moveForward(self) -> None:
        self._position += Camera.MOVEMENT_SPEED * self._viewDirection
        self.update()

    # -------------------------------
    def moveBackward(self) -> None:
        self._position += -Camera.MOVEMENT_SPEED * self._viewDirection
        self.update()

    # -------------------------------
    def moveDown(self) -> None:
        self._position += -Camera.MOVEMENT_SPEED * self._upVector
        self.update()

    # -------------------------------
    def moveUp(self) -> None:
        self._position += Camera.MOVEMENT_SPEED * self._upVector
        self.update()

    # -------------------------------
    def moveRight(self) -> None:
        pass

    # -------------------------------
    def moveLeft(self) -> None:
        pass

    # -------------------------------
    def strafeRight(self) -> None:
        strafeDirection = cross(self._viewDirection, self._upVector)
        self._position += Camera.MOVEMENT_SPEED * strafeDirection

    # -------------------------------
    def strafeLeft(self) -> None:
        strafeDirection = cross(self._viewDirection, self._upVector)
        self._position += -Camera.MOVEMENT_SPEED * strafeDirection

""" Follow object calculations - Turning around object """
"""
# Vertical (90-270)
newPitch = Library.camera.getPitch()
newPitch -= self.MOUSE_SPEED * deltaY
if newPitch >= StartControl.MAX_PITCH:
newPitch = StartControl.MAX_PITCH
elif newPitch <= StartControl.MIN_PITCH:
newPitch = StartControl.MIN_PITCH
else:
pass
Library.camera.setPitch(newPitch)

# Horizontal (-170 - + 170)
newYaw = Library.camera.getYaw()
newYaw += -self.MOUSE_SPEED * deltaX
Library.camera.setYaw(newYaw)
if newYaw >= StartControl.MAX_YAW:
newYaw = StartControl.MAX_YAW
elif newYaw <= StartControl.MIN_YAW:
newYaw = StartControl.MIN_YAW
else:
pass
Library.camera.setYaw(newYaw)
"""

""" Inc/Dec distance from object """
"""
if wheelEvent.angleDelta().y() > 0:
    Camera.DISTANCE_TO_TARGET -= 0.8
else:
    Camera.DISTANCE_TO_TARGET += 0.8
"""

""" Moving object backward """
"""
tPos = self.dae.getPosition()
newXPos = tPos.x - sin(radians(self.dae.getYRotation())) * VObject.MOVEMENT_SPEED
newZPos = tPos.z - cos(radians(self.dae.getYRotation())) * VObject.MOVEMENT_SPEED
self.dae.setPosition(vec3([newXPos, tPos.y, newZPos]))
"""

""" Moving object forward """
"""
tPos = self.dae.getPosition()
newXPos = tPos.x + sin(radians(self.dae.getYRotation())) * VObject.MOVEMENT_SPEED
newZPos = tPos.z + cos(radians(self.dae.getYRotation())) * VObject.MOVEMENT_SPEED
self.dae.setPosition(vec3([newXPos, tPos.y, newZPos]))
"""

""" Turning object right """
# self.dae.setYRotation(self.dae.getYRotation() - 5)

""" Turning object left """
# self.dae.setYRotation(self.dae.getYRotation() + 5)