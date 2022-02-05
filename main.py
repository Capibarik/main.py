# "File Manager" is studying project for learning some libraries and frameworks

from PySide6 import QtWidgets, QtGui, QtCore
from FileManagerDesign import DesignFileManagePy, DialogSaveSetup, DialogCreateDir, DialogRename
import os
import stat
import sys
import psutil
import json


class DialogSaveSetupWin(QtWidgets.QDialog, DialogSaveSetup.Ui_DialogSaveSetup):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)


class DialogCreateDirWin(QtWidgets.QDialog, DialogCreateDir.Ui_dialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

class DialogRenameWin(QtWidgets.QDialog, DialogRename.Ui_dialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)


class FileManagerApp(QtWidgets.QMainWindow, DesignFileManagePy.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.jsonSetup = self.readSetup()
        self.allDisks = self.getLogDisks()
        self.startPaths = [self.jsonSetup["startPaths"][0], self.jsonSetup["startPaths"][1]]
        self.currentPath = [self.startPaths[0], self.startPaths[1]]
        self.currentIndexPath = 0
        self.currentPanel = self.panelDynamic
        self.currentLabel = self.lblCurrentPathDynamic
        self.iconDirItem = QtGui.QIcon(os.getcwd() + "\\PngPicture\\folder.png")
        self.iconFileItem = QtGui.QIcon(os.getcwd() + "\\PngPicture\\google-docs.png")
        self.currentSwap = self.jsonSetup["currentSwap"]  # динамичесая панель слева, а статическая - справа
        self.dialogSaveSetup = DialogSaveSetupWin(self)  # инициализация диалогового окна
        self.dialogCreateDir = DialogCreateDirWin(self)
        self.dialogRename = DialogRenameWin(self)
        self.mBPathError = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Ошибка!", "Путь не найден.", QtWidgets.QMessageBox.Ok) # инициализация окна с сообщением об ошибке
        self.mBNameError = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Ошибка!", "Неверно заданное имя файла.", QtWidgets.QMessageBox.Ok)
        self.mBFolderError2 = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Внимание!", "Выберите, в какой панеле\nбудет создана ваша папка.", QtWidgets.QMessageBox.Ok)
        self.mBChoosePanel = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Внимание!", "Выберите панель.", QtWidgets.QMessageBox.Ok)
        if os.path.exists(self.startPaths[0]) == False:
            self.startPaths[0] = os.getcwd()
        if os.path.exists(self.startPaths[1]) == False:
            self.startPaths[1] = os.getcwd()
        self.ShowDir(panel=self.panelDynamic, path=self.startPaths[0], label=self.lblCurrentPathDynamic)
        self.ShowDir(panel=self.panelStatic, path=self.startPaths[1], label=self.lblCurrentPathStatic)
        self.changeDirFile(item=self.panelDynamic.item(0), text=self.startPaths[0], start=True)
        self.changeDirFile(item=self.panelStatic.item(0), text=self.startPaths[1], start=True)
        self.swapPanels()
        self.comboBoxDynamicP.addItems(self.allDisks)
        self.comboBoxStaticP.addItems(self.allDisks)

        # привязка функций к объектам
        self.panelDynamic.itemDoubleClicked.connect(lambda item: self.changeDirFile(item, item.text()))
        self.panelDynamic.itemPressed.connect(self.curElems)
        self.panelStatic.itemDoubleClicked.connect(lambda item: self.changeDirFile(item, item.text()))
        self.panelStatic.itemPressed.connect(self.curElems)
        self.btnChangePanel.clicked.connect(self.swapPanels)
        self.btnSaveConfigure.clicked.connect(self.dialogSaveSetup.show)
        self.btnUpdate.clicked.connect(self.updateManager)
        self.btnCreateDir.clicked.connect(self.dialogCreateDir.show)
        self.btnDelete.clicked.connect(lambda: self.delDir(self.currentPanel.currentItem()))
        self.btnRename.clicked.connect(self.dialogRename.show)
        self.dialogSaveSetup.accepted.connect(self.saveSetup) # на кнопку OK вешаем действие (сохранение состояния)
        self.dialogCreateDir.accepted.connect(lambda: self.createDir(self.currentPanel.currentItem()))
        self.dialogRename.accepted.connect(lambda: self.renameDir(self.currentPanel.currentItem()))

        # аргумент item в нижних двух строках - это число
        self.comboBoxDynamicP.activated.connect(lambda item: self.changeDirFile(self.panelDynamic.item(0), self.allDisks[item], True))
        self.comboBoxStaticP.activated.connect(lambda item: self.changeDirFile(self.panelStatic.item(0), self.allDisks[item], True))

        # горячие клавиши
        swapPanelShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtGui.Qt.CTRL | QtGui.Qt.Key_U), self.btnChangePanel) # смена панелей местами
        swapPanelShortcut.activated.connect(self.swapPanels)
        openDirFileSc = QtGui.QShortcut(QtGui.QKeySequence(QtGui.Qt.Key_Enter), self.currentPanel)
        openDirFileSc.activated.connect(lambda: self.changeDirFile(self.currentPanel.currentItem(), self.currentPanel.currentItem().text()))
        backDirSc = QtGui.QShortcut(QtGui.QKeySequence(QtGui.Qt.Key_Backspace), self.currentPanel)
        backDirSc.activated.connect(self.backDir)
        backRootDirSc = QtGui.QShortcut(QtGui.QKeySequence(QtGui.Qt.Key_Slash), self.currentPanel)
        backRootDirSc.activated.connect(self.backRootDir)
        renameSc = QtGui.QShortcut(QtGui.QKeySequence(QtGui.Qt.SHIFT | QtGui.Qt.Key_F6), self.currentPanel)
        renameSc.activated.connect(self.dialogRename.show)
        delSc = QtGui.QShortcut(QtGui.QKeySequence(QtGui.Qt.Key_Delete), self.currentPanel)
        delSc.activated.connect(lambda: self.delDir(self.currentPanel.currentItem()))
        createDirSc = QtGui.QShortcut(QtGui.QKeySequence(QtGui.Qt.Key_F7), self.currentPanel)
        createDirSc.activated.connect(self.dialogCreateDir.show)

    def backRootDir(self):
        """Функция горячей клавиши Slash. Возвращение в корневой каталог"""
        currentItem0 = self.currentPanel.item(0)
        if currentItem0.text() == "..":
            rootDir = self.currentPath[self.currentIndexPath].split("\\")[0] + '\\'
            self.ShowDir(self.currentPanel, self.currentLabel, rootDir)
            self.currentPath[self.currentIndexPath] = rootDir

    def backDir(self):
        """Функция горячей клавиши Backspace. Возвращает на каталог выше"""
        currentItem0 = self.currentPanel.item(0)
        if currentItem0.text() == "..":
            self.changeDirFile(currentItem0, currentItem0.text())

    def contextMenuEvent(self, event):
        """Создание и вывод на экран контекстного меню"""
        currentItem = self.currentPanel.currentItem()
        contextMenu = QtWidgets.QMenu(self)
        openFile = QtGui.QAction("Открыть", self)
        openFile.triggered.connect(lambda: self.changeDirFile(currentItem, currentItem.text()))
        renameFile = QtGui.QAction("Переименовать", self)
        renameFile.triggered.connect(self.dialogRename.show)
        copyFile = QtGui.QAction("Копировать", self)
        cutFile = QtGui.QAction("Вырезать", self)
        delFile = QtGui.QAction("Удалить", self)
        delFile.triggered.connect(lambda: self.delDir(currentItem))
        contextMenu.addActions([openFile, renameFile, copyFile, cutFile, delFile])
        contextMenu.exec(event.globalPos())

    def curElems(self, item):
        """Выставление активных элементов файлового менеджера: надписи, панели, индекса и пути"""
        objListWidget = item.listWidget()
        # на следующих трёх строчках будут записываться данные о нахождении пользователя
        self.currentIndexPath = 0  # индекс пути
        self.currentPanel = self.panelDynamic  # текущая панель
        self.currentLabel = self.lblCurrentPathDynamic  # текущая надпись
        if objListWidget == self.panelStatic:
            self.currentIndexPath = 1
            self.currentPanel = self.panelStatic
            self.currentLabel = self.lblCurrentPathStatic

    @staticmethod
    def updateManagerDecor(func):
        """Декоратор для определения пользователя на панелях и обновления менеджера"""
        def newFunc(self, item):
            if item is None:
                self.mBChoosePanel.show()
            else:
                self.curElems(item)
                func(self, item)
                self.updateManager()
        return newFunc

    @updateManagerDecor
    def renameDir(self, item):
        textOld = item.text()
        textNew = self.dialogRename.editLineNameDir.text()
        currentOldNamePath = self.currentPath[self.currentIndexPath] + "\\" + textOld
        currentNewNamePath = self.currentPath[self.currentIndexPath] + "\\" + textNew
        try:
            os.rename(currentOldNamePath, currentNewNamePath)
        except FileExistsError:
            self.mBNameError.show()
        except OSError:
            self.mBNameError.show()

    @updateManagerDecor
    def delDir(self, item):
        """Удаляем (пустую) папку"""
        itemText = item.text()
        delPathFile = self.currentPath[self.currentIndexPath] + "\\" + itemText
        if os.path.isfile(delPathFile): # если файл, удаляем как файл, нет - как папку
            os.remove(delPathFile)
        else:
            os.rmdir(delPathFile)

    @updateManagerDecor
    def createDir(self, item):
        """Создаем папку, выбрасываем ошибку, если неправильно назван файл"""
        nameDir = self.dialogCreateDir.editLineNameDir.text()
        try:
            os.mkdir(self.currentPath[self.currentIndexPath] + "\\" + nameDir)
        except FileExistsError:
            self.mBNameError.show()
        except PermissionError:
            self.mBNameError.show()

    def readSetup(self):
        try:
            with open("C:\\Users\\Алексей\\PycharmProjects\\FileManager\\setup.json", "rt") as setup:
                readSetup = setup.read()
                jsonData = json.loads(readSetup)
            return jsonData
        except FileNotFoundError:
            return {
                "currentSwap": False,
                "startPaths": [os.getcwd(), os.getcwd()],
            }
    def updateManager(self):
        """Обновление данных файлового менеждера"""
        self.allDisks = self.getLogDisks()
        self.comboBoxDynamicP.clear()
        self.comboBoxStaticP.clear()
        self.comboBoxDynamicP.addItems(self.allDisks)
        self.comboBoxStaticP.addItems(self.allDisks)
        self.ShowDir(panel=self.panelDynamic, path=self.currentPath[0], label=self.lblCurrentPathDynamic)
        self.ShowDir(panel=self.panelStatic, path=self.currentPath[1], label=self.lblCurrentPathStatic)

    def saveSetup(self):
        """Сохранение состояния файлового менеджера"""
        self.jsonSetup = {
            "currentSwap": not self.currentSwap,
            "startPaths": [self.currentPath[0], self.currentPath[1]],
        }
        with open("C:\\Users\\Алексей\\PycharmProjects\\FileManager\\setup.json", "wt") as setup:
            jsonData = json.dumps(self.jsonSetup)
            setup.write(jsonData)

    def getLogDisks(self):
        """Получение имён логических дисков"""
        logDisks = psutil.disk_partitions()
        nameDisks = []
        for disk in logDisks:
            nameDisks.append(disk.device)
        return nameDisks

    def deletePointsSlashes(self, pathEx):
        """Удаляем ".." и возвращаем новый путь без "точек" и беконченого количества слешей"""
        newPath = QtCore.QDir.cleanPath(pathEx).replace("/", "\\")
        return newPath

    def limLenLbl(self, pathEx):
        """Длинные пути (свыше 56 символов) будут сокращаться путём замены ближних к корневой папке директорий
        на точки ("...")"""
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

    def isHiddenFile(self, pathToFile):
        """True - файл невидим, False - файл видим"""
        # проверка существования пути
        if pathToFile in self.allDisks:
            return False
        else:
            return bool(os.stat(pathToFile).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

    def changeDirFile(self, item, text, isChD=False, start=False):
        """Смена директории или файла. Прибавляем к пути название файла,
        если же хотим вернуться назад, то прибавляем '..'. В начале функции узнаём, откуда
        произошел её вызов, и в соответствие с этим выбираем панель"""
        self.curElems(item)
        curLP, curPanel, indexCP = self.currentLabel, self.currentPanel, self.currentIndexPath
        choosePath = text
        # создание нормального пути (без "..") и проверка его на существование
        if isChD: # isChD - хочет ли пользователь поменять диск {True; False}
            isFileExist = os.path.exists(text)
            if isFileExist: # если диск существует (еще подключен)
                self.currentPath[indexCP] = text
            else:
                self.currentPath[indexCP] = self.startPaths[indexCP]
                self.mBPathError.show()
                print("Диск")
        else:
            currentPathTemp = self.createRPath(indexCP, choosePath)
            if start: # если идет запуск приложения, то нормальный путь - это стартовый путь
                currentPathTemp = self.startPaths[indexCP]
            else:
                if currentPathTemp is not None: # если файл существует
                    isHFResult = self.isHiddenFile(currentPathTemp) # является ли файл скрытым
                    if isHFResult == False:
                        self.currentPath[indexCP] = currentPathTemp
                else:
                    # если пути не существует, то возвращаем пользователя на стартовый путь и показывем соответствующее сообщение
                    self.currentPath[indexCP] = self.startPaths[indexCP]
                    self.mBPathError.show()
        isFCP = os.path.isfile(self.currentPath[indexCP])
        if isFCP:
            try:
                os.startfile(self.currentPath[indexCP])
            except OSError as text:
                print(text, "\n", self.changeDirFile.__doc__)
            self.currentPath[indexCP] = "\\".join(self.currentPath[indexCP].split("\\")[:-1]) # удаляем файл из пути
        else:
            self.ShowDir(panel=curPanel, path=self.currentPath[indexCP], label=curLP)
        os.chdir(self.currentPath[indexCP]) # меняем директорию реально

    def createRPath(self, indexCP, choosePath):
        """Создание нормального путя, т.е. без ".." и двойных обратных слешей"""
        sep = ""
        if self.currentPath[indexCP] not in self.allDisks:
            sep = "\\"
        curTempPath = self.currentPath[indexCP] + sep + choosePath
        isExist = os.path.exists(curTempPath)
        if isExist:
            return self.deletePointsSlashes(curTempPath)

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
            self.comboBoxLayout.removeWidget(self.comboBoxStaticP)
            self.comboBoxLayout.removeWidget(self.comboBoxDynamicP)
            self.comboBoxLayout.addWidget(self.comboBoxStaticP)
            self.comboBoxLayout.addWidget(self.comboBoxDynamicP)
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
            self.comboBoxLayout.removeWidget(self.comboBoxDynamicP)
            self.comboBoxLayout.removeWidget(self.comboBoxStaticP)
            self.comboBoxLayout.addWidget(self.comboBoxDynamicP)
            self.comboBoxLayout.addWidget(self.comboBoxStaticP)
            self.currentSwap = True

def main():
    app = QtWidgets.QApplication(sys.argv)
    fm = FileManagerApp()
    fm.show()
    app.exec()

if __name__ == "__main__":
    main()
