# encoding: utf-8

# System
import os

# Extern library
import sqlite3
import numpy as np
from OpenGL.GL import GLuint, GLfloat, GLushort

# DAL Inner
from libs.OpenGL.DAL.Inner.rawobject import RawObject


# ----------------------------------------------
class SqliteControl:
# ----------------------------------------------
   """ Summary
   """
   # ----------------------------------------------
   def __init__(self, dir_s: str, filename_s: str):
   # ----------------------------------------------
      try:
         completePath_s = os.path.join(dir_s, filename_s)
         self.conn = sqlite3.connect(completePath_s)
         if not self.conn:
            return

      except Exception as ex:
         print(f"Not implemented exception. {self.__class__} {__name__} :: {str(ex)}")


# ----------------------------------------------
class DataControl(SqliteControl):
# ----------------------------------------------
   """ Summary
   """

   NAME_LOC = 0

   V_LOC = 1
   I_LOC = 2
   N_LOC = 3
   T_LOC = 4
   T_FILES_LOC = 5

   SHADER_NAME_LOC = 6

   # ----------------------------------------------
   def __init__(self, dir_s: str, filename_s: str):
   # ----------------------------------------------
      super(DataControl, self).__init__(dir_s, filename_s)

   # ----------------------------------------------
   def getRawObject(self, name_s: str) -> RawObject:
   # ----------------------------------------------
      rawObject_o = RawObject()
      try:
         cursor = self.conn.cursor()
         # TODO Security check!
         selectQuery = f"select * from data where name='{name_s}';"
         reader = cursor.execute(selectQuery)
         for row in reader:
            rawObject_o.name = str(row[DataControl.NAME_LOC])

            rawObject_o.vertexCoords = np.array(str(row[DataControl.V_LOC]).split(','), dtype=GLfloat)
            rawObject_o.indices = np.array(str(row[DataControl.I_LOC]).split(','), dtype=GLushort)
            rawObject_o.normalCoords = np.array(str(row[DataControl.N_LOC]).split(','), dtype=GLfloat)
            rawObject_o.textureCoords = np.array(str(row[DataControl.T_LOC]).split(','), dtype=GLfloat)
            rawObject_o.textureFiles = str(row[DataControl.T_FILES_LOC]).split(";")

            rawObject_o.shaderName = str(row[DataControl.SHADER_NAME_LOC])

      except Exception as ex:
         print(f"Not implemented exception. {self.__class__} {__name__} :: {str(ex)}")

      return rawObject_o
