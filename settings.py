import sys
from custome_errors import *
sys.excepthook = my_excepthook
import os
import settings_handler
import language
import PyQt6.QtWidgets as qt
import sys
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
class main (qt.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("settings"))
        self.alang={
            "arabic":"ar",
            "english":"en",
            "spanish":"es",
            "romanian":"ro",
            "french":"fr"
        }
        label=qt.QLabel(_("language"))
        self.language=qt.QComboBox()
        self.language.setAccessibleName(_("app language"))
        self.language.addItems(language.lang().keys())
        languages = {index:language for language, index in enumerate(language.lang().values())}
        try:
            self.language.setCurrentIndex(languages[settings_handler.get("g","lang")])
        except Exception as e:
            self.language.setCurrentIndex(0)
        self.ttslang=qt.QComboBox()
        self.ttslang.addItems(self.alang.keys())
        languages1 = {index:language for language, index in enumerate(self.alang.values())}
        try:
            self.ttslang.setCurrentIndex(languages1[settings_handler.get("g","langtts")])
        except:
            self.ttslang.setCurrentIndex(0)
        self.ttslang.setAccessibleName(_("listen to respons language"))
        self.ok=qt.QPushButton(_("OK"))
        self.ok.clicked.connect(self.fok)
        self.cancel=qt.QPushButton(_("cancel"))
        self.cancel.clicked.connect(self.fcancel)
        layout=qt.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.language)
        layout.addWidget(self.ttslang)
        layout.addWidget(self.ok)
        layout.addWidget(self.cancel)
        self.setLayout(layout)
    def fok(self):
        settings_handler.set("g","lang",str(language.lang()[self.language.currentText()]))
        settings_handler.set("g","langtts",str(self.alang[self.ttslang.currentText()]))
        mb=qt.QMessageBox()
        mb.setWindowTitle(_("settings updated"))
        mb.setText(_("you must restart the program to apply changes \n do you want to restart now?"))
        rn=mb.addButton(qt.QMessageBox.StandardButton.Yes)
        rn.setText(_("restart now"))
        rl=mb.addButton(qt.QMessageBox.StandardButton.No)
        rl.setText(_("restart later"))
        mb.exec()
        ex=mb.clickedButton()
        if ex==rn:
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif ex==rl:
            self.close()
    def fcancel(self):
        self.close()
    def cbts(self,string):
        if string=="True":
            return True
        else:
            return False


