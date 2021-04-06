# encoding: utf-8
from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from libs.Qt.vglwidget import VGLWidget
    from libs.OpenGL.DataLoader.dataloader import DataLoader
    from PyQt5.QtWidgets import QApplication
    from libs.OpenGL.camera import Camera
    from datetime import datetime



class Library:
    loader = None
    app: QApplication = None
    mainWindow: VGLWidget = None
    camera: Camera = None
    libs = {""}

    # Map
    vMap = None

    processes = []

    beforeStart_o: datetime = None
    afterStart_o: datetime = None
