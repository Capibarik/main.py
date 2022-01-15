# "File Manager" is studying project for learning some libraries and frameworks

from PySide6 import QtWidgets, QtGui, QtCore
from FileManagerDesign import DesignFileManagePy, DialogSaveSetup
import os
import sys
import psutil
import json


class DialogSaveSetupWin(QtWidgets.QDialog, DialogSaveSetup.Ui_DialogSaveSetup):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)


class FileManagerApp(QtWidgets.QMainWindow, DesignFileManagePy.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.jsonSetup = self.readSetup()
        # --file
        self.allDisks = self.getLogDisks()
        self.startPaths = [os.getcwd(), "C:\\"]
        self.currentPath = [self.startPaths[0], self.startPaths[1]]
        # --not file
        self.currentIndexPath = 0
        self.currentPanel = self.panelDynamic
        self.currentLabel = self.lblCurrentPathDynamic
        # --not file
        self.iconDirItem = QtGui.QIcon("C:\\Users\\Алексей\\PycharmProjects\\FileManager\\PngPicture\\folder.png")
        self.iconFileItem = QtGui.QIcon("C:\\Users\\Алексей\\PycharmProjects\\FileManager\\PngPicture\\google-docs.png")
        self.currentSwap = self.jsonSetup["currentSwap"]  # динамичесая панель слева, а статическая - справа
        # file--
        self.dialog = DialogSaveSetupWin(self)  # инициализация диалогового окна
        self.ShowDir(panel=self.panelDynamic, path=self.startPaths[0], label=self.lblCurrentPathDynamic)
        self.ShowDir(panel=self.panelStatic, path=self.startPaths[1], label=self.lblCurrentPathStatic)
        self.swapPanels()
        # привязка функций к объектам
        self.panelDynamic.itemDoubleClicked.connect(self.changeDirFile)
        self.panelDynamic.itemClicked.connect(self.curElems)
        self.panelStatic.itemDoubleClicked.connect(self.changeDirFile)
        self.panelStatic.itemClicked.connect(self.curElems)
        self.btnChangePanel.clicked.connect(self.swapPanels)
        self.btnSaveConfigure.clicked.connect(self.showDialogSaveSetup)
        self.dialog.accepted.connect(self.saveSetup)
        # горячие клавиши
        # смена панелей местами
        swapPanelShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtGui.Qt.CTRL | QtGui.Qt.Key_U), self.btnChangePanel)
        swapPanelShortcut.activated.connect(self.swapPanels)
        openDirFileSc = QtGui.QShortcut(QtGui.QKeySequence(QtGui.Qt.Key_O), self.currentPanel)
        openDirFileSc.activated.connect(lambda: self.changeDirFile(self.currentPanel.currentItem()))
        backDirSc = QtGui.QShortcut(QtGui.QKeySequence(QtGui.Qt.Key_Backspace), self.currentPanel)
        backDirSc.activated.connect(self.backDir)

    def backDir(self):
        """Функция горячей клавиши Backspace. Возвращает на каталог выше"""
        currentItem0 = self.currentPanel.item(0)
        if currentItem0.text() == "..":
            self.changeDirFile(currentItem0)

    def readSetup(self):
        try:
            with open(os.getcwd() + "\\" + "setup.json", "rt") as setup:
                readSetup = setup.read()
                jsonData = json.loads(readSetup)
            return jsonData
        except FileNotFoundError:
            return {"currentSwap": False}

    def saveSetup(self):
        self.jsonSetup = {"currentSwap": not self.currentSwap}
        with open(os.getcwd() + "\\" + "setup.json", "wt") as setup:
            jsonData = json.dumps(self.jsonSetup)
            setup.write(jsonData)

    def getLogDisks(self):
        """Получение имён логических дисков"""
        logDisks = psutil.disk_partitions()
        nameDisks = []
        for disk in logDisks:
            nameDisks.append(disk.device)
        return nameDisks

    def showDialogSaveSetup(self):
        self.dialog.show()

    def deletePointsSlashes(self, pathEx):
        """Удаляем ".." и возвращаем новый путь без "точек" и беконченого количества слешей"""
        newPath = QtCore.QDir.cleanPath(pathEx).replace("/", "\\")
        return newPath

    def limLenLbl(self, pathEx):
        """Длинные пути (свыше 56 символов) будут сокращаться путём замены ближних к корневой папке директорий
        на символы точек ("...")"""
        newPath = pathEx
        i = 1
        while len(newPath) > 50 and i < len(newPath.split("\\")) - 1:
            pathList = newPath.split("\\")
            pathList[i] = "..."
            newPath = "\\".join(pathList)
            i += 1
        return newPath

    def ShowDir(self, panel, label, path):
        """Вывод директории, узнавая путь до неё и выводя всё, что находится в ней, на экран"""
        panel.clear()
        pathfLbl = self.limLenLbl(path)
        label.setText(pathfLbl)
        directory = os.listdir(path)
        if not (path in (self.allDisks)):
            panel.addItem("..")
        for file in directory:
            isFile = os.path.isfile(path + "\\" + file)
            if isFile:
                currentIcon = self.iconFileItem
            else:
                currentIcon = self.iconDirItem
            panelWidgets = QtWidgets.QListWidgetItem()
            panelWidgets.setText(file)
            panelWidgets.setIcon(currentIcon)
            panel.addItem(panelWidgets)

    def changeDirFile(self, item):
        """Смена директории или файла. Прибавляем к пути название файла,
        если же хотим вернуться назад, то прибавляем '..'. В начале функции узнаём, откуда
        произошел её вызов, и в соответствие с этим выбираем панель"""
        self.curElems(item)
        curLP, curPanel, indexCP = self.currentLabel, self.currentPanel, self.currentIndexPath
        choosePath = item.text()
        # создание нормального путя (без "..")
        self.currentPath[indexCP] = self.createRPath(indexCP, choosePath)
        isFCP = os.path.isfile(self.currentPath[indexCP])
        if isFCP:
           os.startfile(self.currentPath[indexCP])
           self.currentPath[indexCP] = "\\".join(self.currentPath[indexCP].split("\\")[:-1]) # удаляем файл из пути
        else:
            self.ShowDir(panel=curPanel, path=self.currentPath[indexCP], label=curLP)

    def curElems(self, item):
        """Выставление активных элементов файлового менеджера: надписи, панели, индекса и пути"""
        objListWidget = item.listWidget()
        # на следующих трёх строчках в файл будут записываться данные о нахождении пользователя
        self.currentIndexPath = 0  # индекс пути
        self.currentPanel = self.panelDynamic  # текущая панель
        self.currentLabel = self.lblCurrentPathDynamic  # текущая надпись
        if objListWidget == self.panelStatic:
            self.currentIndexPath = 1
            self.currentPanel = self.panelStatic
            self.currentLabel = self.lblCurrentPathStatic

    def createRPath(self, indexCP, choosePath):
        """Создание нормального путя, т.е. без ".." и двойных обратных слешей"""
        sep = ""
        if self.currentPath[indexCP] not in self.allDisks:
            sep = "\\"
        curTmpPath = self.currentPath[indexCP] + sep + choosePath
        isExist = os.path.exists(curTmpPath)
        if isExist:
            return self.deletePointsSlashes(curTmpPath)

    def swapPanels(self):
        """Меняем местами панели и их надписи с текущими путями."""
        if self.currentSwap:
            self.LayoutPanels.removeWidget(self.panelStatic)
            self.LayoutPanels.removeWidget(self.panelDynamic)
            self.LayoutPanels.addWidget(self.panelStatic)
            self.LayoutPanels.addWidget(self.panelDynamic)
            self.CurrentPathsLabels.removeWidget(self.lblCurrentPathStatic)
            self.CurrentPathsLabels.removeWidget(self.lblCurrentPathDynamic)
            self.CurrentPathsLabels.addWidget(self.lblCurrentPathStatic)
            self.CurrentPathsLabels.addWidget(self.lblCurrentPathDynamic)
            self.currentSwap = False
        else:
            self.LayoutPanels.removeWidget(self.panelDynamic)
            self.LayoutPanels.removeWidget(self.panelStatic)
            self.LayoutPanels.addWidget(self.panelDynamic)
            self.LayoutPanels.addWidget(self.panelStatic)
            self.CurrentPathsLabels.removeWidget(self.lblCurrentPathDynamic)
            self.CurrentPathsLabels.removeWidget(self.lblCurrentPathStatic)
            self.CurrentPathsLabels.addWidget(self.lblCurrentPathDynamic)
            self.CurrentPathsLabels.addWidget(self.lblCurrentPathStatic)
            self.currentSwap = True

def main():
    app = QtWidgets.QApplication(sys.argv)
    fm = FileManagerApp()
    fm.show()
    app.exec()

if __name__ == "__main__":
    main()
