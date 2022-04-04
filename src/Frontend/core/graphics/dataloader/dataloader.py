# encoding: utf-8

# System
import os

# models ram
from openal import oalGetListener

from core.graphics.models.ram.rawobject import RawObject
# Libraries
from core.graphics.models.vram.vcubemap import VCubeMap
# Local
from core.graphics.models.vram.vsimpledae import VSimpleDae
from core.graphics.models.vram.vsimplemap import VSimpleMap
from core.graphics.models.vram.vsoundbox import VSoundBox
from core.graphics.dataloader.sqlitecontrol import DataControl
# Global
from settings import *


# -----------------
class DataLoader:
    """ Summary
       Main interface between user and objects
       and objects and its raw data
       User -> graphics card  -> VOpenGL object -> RAM -> RawObject -> physical data from disk
    """
    LIBRARY = dict()

    # Database information
    DATA_PREFIX = "data"
    DATA_SUFFIX = ".sqlite"
    DATA_LOGIN = ""

    DEFAULT_SHADER_NAME = "model"

    dataInformation_o = None
    dataController_o = None

    # -----------------
    def __init__(self):
        try:
            self.__dataInformation_o = Settings.dataSettings
            fullPath_s = os.path.join(os.getcwd(), self.__dataInformation_o["path"])
            self.__dataController_o = DataControl(fullPath_s, DataLoader.DATA_PREFIX + DataLoader.DATA_SUFFIX)

            self.__modelShader = None
            self.__mapShader = None

        except Exception as ex:
            print(f"__init__(): DataLoader [ERROR] {ex.args}")
        # return None

    def getSimpleMap(self, mapName: str, length: int, dividor:int, textureFilename: str) -> VSimpleMap or None:
        rawScaledMap = RawObject()
        if rawScaledMap.loadMap(length, dividor) == -1:
            return None

        return VSimpleMap(mapName, rawScaledMap, textureFilename)

    def getSimpleDaeObject(self, daeName: str, filename_s: str, texture) -> VSimpleDae or None:
        rawObject = RawObject()
        if rawObject.loadDAE(filename_s) == -1:
            return None

        return VSimpleDae(daeName, rawObject, texture)

    def getVCubeMap(self, size_i, textureDir_s) -> VCubeMap or None:
        rawCube = RawObject()
        rawCube.loadCube(size_i)
        if rawCube is None:
            return None

        return VCubeMap(rawCube, textureDir_s)


    def getSoundBox(self, soundFile_s):
        rawCube = RawObject()
        if rawCube.loadDAE("TestQuad/testQuad.dae") == -1:
            return None

        return VSoundBox(rawCube, "altebirke.jpg", oalGetListener(), soundFile_s, True)

















