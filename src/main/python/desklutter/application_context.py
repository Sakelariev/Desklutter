from fbs_runtime.application_context import ApplicationContext, \
    cached_property
import sys
import schedule
import time
import os
import shutil
from datetime import datetime as dt
import threading
import platform
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QInputDialog, QLineEdit, QSystemTrayIcon, QMenu, QAction)
# import logging
# logging.basicConfig(filename='desklutter.log',level=logging.DEBUG)



# Adding the UI
qtCreatorFile = "widget.ui"
#Get desktop path on Mac
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
#get all files and folders on Desktop
all_files = os.listdir(desktop)
to_move = []
system_files = []





class AppContext(ApplicationContext):
    def run(self):
        self.window.show()
        self.tray_icon.show()
        return self.app.exec_()

#Don't cache this please
    def closeApp(self):
        return sys.exit()


#Don't cache this please
    def showWindow(self):
        return self.window.show()

    @cached_property
    def window(self):
        Ui_MainWindow, QtBaseClass = uic.loadUiType(self.get_resource(qtCreatorFile))
        class MyApp2(MyApp, Ui_MainWindow):
            pass
        return MyApp2()
    @cached_property
    def app(self):
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        return app
    @cached_property
    def icon(self):
        return QIcon(self.get_resource('icon-menu.png'))
    @cached_property
    def action(self):
        turn_on = QAction("Open Desklutter")
        turn_on.triggered.connect(self.showWindow)
        return turn_on
    @cached_property
    def action2(self):
        quit = QAction("Quit")
        quit.triggered.connect(self.closeApp)
        return quit
    @cached_property
    def menuTray(self):
        menu = QMenu()
        menu.addAction(self.action)
        menu.addAction(self.action2)
        return menu
    @cached_property
    def tray_icon(self):
        tray = QSystemTrayIcon()
        tray.setIcon(self.icon)
        tray.setVisible(True)
        tray.setContextMenu(self.menuTray)
        return tray


class MyApp(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loopFiles()
        self.startButton.clicked.connect(self.setSchedule)
        self.startButton.clicked.connect(self.hideWindow)
        self.startButton.clicked.connect(self.disablePicker)
        self.startButton.clicked.connect(self.disableButton)
        self.startButton.clicked.connect(self.enableCheckbox)
        self.checkBox.clicked.connect(self.resetSchedule)

    def enableCheckbox(self):
        return self.checkBox.setEnabled(True)

    def disablePicker(self):
        return self.timeBegin.setDisabled(True)

    def disableButton(self):
        return self.startButton.setDisabled(True)

    def hideWindow(self):
        return self.close()

    def resetSchedule(self):
        schedule.clear()
        self.startButton.setEnabled(True)
        self.timeBegin.setEnabled(True)


    #Create a folder if it doesn't exist already
    def createFolder(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)

        except OSError:
            print ('Error:Creating directory - ' + directory)


    def moveFiles(self):
        for e in to_move:
            if e == 'Declutter':
                pass
            else:
                print(e)
                path = os.path.join(desktop, e)
                print(path)
                shutil.move(path, desktop + '/Declutter/')


    createFolder(desktop + '/Declutter/')

    def loopFiles(self):
        for f in all_files:
            if f.startswith('.'):
                system_files.append(f)
            else:
                to_move.append(f)
        print("System files: ", system_files)
        print("To move: ", to_move)


    def setSchedule(self):

        choose_s = self.timeBegin.time()
        choose_start = choose_s.toString()
        choose_start = choose_start[:-3]
        print("Choose start time: ", choose_start)

        schedule.every().day.at(choose_start).do(self.moveFiles)
        ScheduleThread().start()




class ScheduleThread(threading.Thread):
    def __init__(self, *pargs, **kwargs):
        super().__init__(*pargs, daemon=True, name="scheduler", **kwargs)

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(schedule.idle_seconds())
