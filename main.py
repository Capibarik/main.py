# "File Manager" is studying project for learning some libraries and frameworks

from PySide6 import QtWidgets
from FileManagerDesign import DesignFileManagePy
import os
import sys


class FileManagerApp(QtWidgets.QMainWindow, DesignFileManagePy.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.startPaths = ["C:\\", "D:\\"]
        self.ShowDirectory(panel=self.panelDynamic, path=self.startPaths[0])
        self.ShowDirectory(panel=self.panelStatic, path=self.startPaths[1])

    def ShowDirectory(self, panel, path="C:\\"):
        panel.clear()
        directory = os.listdir(path)
        for file in directory:
            panel.addItem(file)


def main():
    app = QtWidgets.QApplication(sys.argv)
    fm = FileManagerApp()
    fm.show()
    app.exec()

if __name__ == "__main__":
    main()
