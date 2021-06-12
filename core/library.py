# encoding: utf-8

class Library:
    loader = None
    app: None
    mainWindow = None
    camera = None
    libs = {""}

    # Map
    vMap = None

    processes = []

    beforeStart_o = None
    afterStart_o = None
