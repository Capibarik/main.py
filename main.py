# "File Manager" is studying project for learning some libraries and frameworks

from PySide6 import QtWidgets, QtCore, QtGui
from FileManagerDesign import DesignFileManagePy
import os
import sys


class FileManagerApp(QtWidgets.QMainWindow, DesignFileManagePy.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.startPaths = ["C:\\", "D:\\"]
        self.currentPath = [self.startPaths[0], self.startPaths[1]]
        self.iconDirItem = QtGui.QIcon("C:\\Рабочий_стол\\Иконки_(Icon)\\cancel.png")
        self.ChooseDirectory(panel=self.panelDynamic, path=self.startPaths[0])
        self.ChooseDirectory(panel=self.panelStatic, path=self.startPaths[1])
        self.panelDynamic.itemDoubleClicked.connect(self.changeDirFile)
        self.panelStatic.itemDoubleClicked.connect(self.changeDirFile)

    def isShowDoublePoints(self, pathEx):
        """Разность между кол-вом директорий в пути и кол-вом "..". Если "точек" будет больше,
        то это значит, что мы вернулись в корневую папку, и возвращаем True, иначе False"""
        pathExList = pathEx.split("\\")[1:]
        quantityDP = pathExList.count("..")
        quantityF = len(pathExList) - quantityDP
        if quantityDP >= quantityF:
            return True
        else:
            return False

    def ChooseDirectory(self, panel, path="C:\\"):
        """Выбор директории, узнавая путь до неё и выводя всё, что находится в ней, на экран"""
        # isFile = os.path.isfile(path)
        # if isFile:
        #     os.startfile(path)
        # else:
        panel.clear()
        directory = os.listdir(path)
        isSDP = self.isShowDoublePoints(path)
        if not ((path in ("C:\\", "D:\\")) or isSDP):
            panel.addItem("..")
        for file in directory:
            panelWidgets = QtWidgets.QListWidgetItem()
            panelWidgets.setText(file)
            panelWidgets.setIcon(self.iconDirItem)
            panel.addItem(panelWidgets)

    @QtCore.Slot()
    def changeDirFile(self, item):
        """Смена директории или файла. Прибавляем к пути название файла,
        если же хотим вернуться назад, то прибавляем '..'"""
        sep = ""
        choosePath = item.text()
        if self.currentPath[0] not in self.startPaths:
            sep = "\\"
        self.currentPath[0] += sep + choosePath
        isFCP = os.path.isfile(self.currentPath[0])
        if isFCP:
           os.startfile(self.currentPath[0])
           self.currentPath[0] = "\\".join(self.currentPath[0].split("\\")[:-1]) # удаляем файл из пути
        else:
            self.ChooseDirectory(panel=self.panelDynamic, path=self.currentPath[0])

def main():
    app = QtWidgets.QApplication(sys.argv)
    fm = FileManagerApp()
    fm.show()
    app.exec()

if __name__ == "__main__":
    main()
