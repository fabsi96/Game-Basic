# encoding: utf-8

# System
import os

# Extern library
import sqlite3
import numpy as np
from OpenGL.GL import GLuint

# DAL Inner
from libs.OpenGL.DAL.Inner.rawobject import RawObject


class SqliteControl:

   def __init__(self, dir_s, filename_s):
      try:
         completePath_s = os.path.join(dir_s, filename_s)
         self.conn = sqlite3.connect(completePath_s)
         if not self.conn:
            return

      except Exception as ex:
         print("Exception :: {0}".format(str(ex)))


class DataControl(SqliteControl):
   NAME_LOC = 0

   V_LOC = 1
   I_LOC = 2
   N_LOC = 3
   T_LOC = 4
   T_FILES_LOC = 5

   SHADER_NAME_LOC = 6

   def __init__(self, dir_s, filename_s):
      super(DataControl, self).__init__(dir_s, filename_s)

   def getRawData(self, name_s):
      rawObject_o = RawObject()
      try:
         cursor = self.conn.cursor()
         selectQuery = "select * from data where name='{0}';".format(name_s)
         reader = cursor.execute(selectQuery)
         for row in reader:
            rawObject_o.name = str(row[DataControl.NAME_LOC])

            rawObject_o.vertexCoords = np.array(str(row[DataControl.V_LOC]).split(','), dtype=np.float32)
            rawObject_o.indices = np.array(str(row[DataControl.I_LOC]).split(','), dtype=GLuint)
            rawObject_o.normalCoords = np.array(str(row[DataControl.N_LOC]).split(','), dtype=np.float32)
            rawObject_o.textureCoords = np.array(str(row[DataControl.T_LOC]).split(','), dtype=np.float32)
            rawObject_o.textureFiles = str(row[DataControl.T_FILES_LOC]).split(";")

            rawObject_o.shaderName = str(row[DataControl.SHADER_NAME_LOC])

      except Exception as ex:
         print("Exception :: {0}".format(str(ex)))

      return rawObject_o
