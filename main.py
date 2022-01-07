# "File Manager" is studying project for learning some libraries and frameworks

from PySide6 import QtWidgets, QtGui
from FileManagerDesign import DesignFileManagePy
import os
import sys


class FileManagerApp(QtWidgets.QMainWindow, DesignFileManagePy.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # --file--
        self.allDisks = ["C:\\", "D:\\"]
        self.startPaths = ["C:\\Рабочий_стол", "D:\\"]
        self.currentPath = [self.startPaths[0], self.startPaths[1]]
        self.currentIndexPath = 0
        self.currentPanel = self.panelDynamic
        self.currentLabel = self.lblCurrentPathDynamic
        self.iconDirItem = QtGui.QIcon("C:\\Users\\Алексей\\PycharmProjects\\FileManager\\PngPicture\\folder.png")
        self.iconFileItem = QtGui.QIcon("C:\\Users\\Алексей\\PycharmProjects\\FileManager\\PngPicture\\google-docs.png")
        # --file--
        self.ShowDir(panel=self.panelDynamic, path=self.startPaths[0], label=self.lblCurrentPathDynamic)
        self.ShowDir(panel=self.panelStatic, path=self.startPaths[1], label=self.lblCurrentPathStatic)
        self.panelDynamic.itemDoubleClicked.connect(self.changeDirFile)
        self.panelDynamic.itemClicked.connect(self.curElems)
        self.panelStatic.itemDoubleClicked.connect(self.changeDirFile)
        self.panelStatic.itemClicked.connect(self.curElems)
        self.commandLine.returnPressed.connect(self.doCommand)

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

    def deletePoints(self, pathEx):
        """Удаляем ".." и возвращаем новый путь без "точек"."""
        pathExList = pathEx.split("\\")
        newPath = pathEx
        if pathExList[-1] == "..":
            newPath = "\\".join(pathExList[:-2])
            allDiskswS = tuple(map(lambda e: e[:-1], self.allDisks)) # диски без слешей (только названия)
            # если конечный путь будет одним из имен дисков, то нужно будет прибавить к пути слеш
            if newPath in allDiskswS:
                newPath += "\\"
        return newPath

    def limLenLbl(self, pathEx):
        """Длинные пути (свыше 56 символов) будут сокращаться путём замены ближних к корневой папке директорий
        на символы точек ("...")"""
        newPath = pathEx
        i = 1
        while len(newPath) > 50:
            pathList = newPath.split("\\")
            pathList[i] = "..."
            newPath = "\\".join(pathList)
            i += 1
        return newPath

    def ShowDir(self, panel, label, path):
        """Вывод директории, узнавая путь до неё и выводя всё, что находится в ней, на экран"""
        panel.clear()
        os.chdir(path) # меняем директорию реально
        pathfLbl = self.limLenLbl(path)
        label.setText(pathfLbl)
        directory = os.listdir(path)
        isSDP = self.isShowDoublePoints(path)
        if not ((path in ("C:\\", "D:\\")) or isSDP):
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
        curLP, curPanel, indexCP = self.curElems(item)
        choosePath = item.text()
        # создание нормального путя (без "..")
        self.createRPath(indexCP, choosePath)
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
        # переменные посредине - это короткие название переменных справа
        self.currentIndexPath = indexCP = 0  # индекс путя
        self.currentPanel = curPanel = self.panelDynamic  # текущая панель
        self.currentLabel = curLP = self.lblCurrentPathDynamic  # текущая надпись
        if objListWidget == self.panelStatic:
            self.currentIndexPath = indexCP = 1
            self.currentPanel = curPanel = self.panelStatic
            self.currentLabel = curLP = self.lblCurrentPathStatic
        return curLP, curPanel, indexCP

    def createRPath(self, indexCP, choosePath):
        """Создание нормального путя, т.е. без ".." и двойных обратных слешей"""
        sep = ""
        if self.currentPath[indexCP] not in self.allDisks:
            sep = "\\"
        curTmpPath = self.currentPath[indexCP] + sep + choosePath
        isExist = os.path.exists(curTmpPath)
        command, param, _ = self.splitCommand()
        if isExist and not param.count(".") > 2 and command in ("cd", "chdir"):
            self.currentPath[indexCP] = curTmpPath
            self.currentPath[indexCP] = self.deletePoints(self.currentPath[indexCP])

    def doCommand(self):
        """Введение команд. Особенно команды cd (chdir).
        Разделяем команду cd на две части: саму команду и её параметр.
        Если же команда не cd (chdir), то просто выполняем её.
        В конце очищаем командную строку и показываем результат команды."""
        command, param, stcom = self.splitCommand()
        # если будет команда переместиться еще выше корневых каталогов, то нужно это предусмотреть
        if param == ".." and self.currentPath[self.currentIndexPath] in self.allDisks:
            param = ""
        match command:
            case "cd" | "chdir":
                self.createRPath(self.currentIndexPath, param)
            case _:
                os.system(stcom)
        self.ShowDir(panel=self.currentPanel, path=self.currentPath[self.currentIndexPath], label=self.currentLabel)
        self.commandLine.setText("")

    def splitCommand(self):
        """Разделяем команду на саму команду, её имя, и параметр.
        Подходит только для команд с одним параметром, в частности для CD/CHDIR"""
        stcom = self.commandLine.text()  # начальная команда
        stcoml = stcom.split(" ")
        try:
            stcoml[1] = " ".join(stcoml[1:])
            del stcoml[2:]
            command = stcoml[0].lower()  # берём только команду (без параметров)
            param = stcoml[1]  # параметр команды
            return command, param, stcom
        except IndexError:
            return "echo", "", "echo"


def main():
    app = QtWidgets.QApplication(sys.argv)
    fm = FileManagerApp()
    fm.show()
    app.exec()

if __name__ == "__main__":
    main()
