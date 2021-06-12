# coding: utf-8
from threading import Thread

from src.start.control import StartControl
from core.library import Library


# ------------------
class StartView:
    """ Summary
       1) Create VObject and do settings on it
       2) Set it into map (with collision system) and /- or to 'master'-renderer (vglwindow)
       3) optional: keep track of it and use it in user-interaction (3rd player view)
    """

    # ------------------
    def __init__(self, loader, window):
        try:
            self.window = window
            # Init controller interface
            self.controller = StartControl(loader, window)

            retVal_o = -1  # self.window.loadUi("test.ui")
            if retVal_o == -1:
                print(f"__init__: StartView [DEBUG] Could not load UI.")
            else:
                self.window.pushBtn1.clicked.connect(self.myButtonClick)

            self.handleThreads = []
        except Exception as ex:
            print(f"__init__: StartView [ERROR] {ex.args}")

    # ------------------
    def start(self, targetFunc=None, *args):
        try:
            if targetFunc is None:
                return -1
            else:
                t = Thread(target=targetFunc, args=[*args, ])
                self.handleThreads.append(t)
                t.start()
        except:
            raise

    # ------------------
    def myButtonClick(self):
        try:
            self.start(self.myButtonWorker, "Hello World!")
        except  Exception as ex:
            print(f"myButtonClick: StartView [ERROR] {ex.args}")

    # ------------------
    def myButtonWorker(self, text: str):
        try:
            self.window.textEdit1.append(text)
        except Exception as ex:
            self.window.textEdit1.append(str(ex))


# ------------------
def main():
    try:
        startView = StartView(Library.loader, Library.mainWindow)
    except Exception as ex:
        print(f"main: view.py [ERROR] {ex.args}")


# ------------------
if __name__ == "__main__":
    main()
