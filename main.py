import sys
from custome_errors import *
sys.excepthook = my_excepthook
from webbrowser import open as openLink
import settings_handler
import winsound
import threading
import pyperclip
import settings
import openai
import app
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
import language
language.init_translation()
chatm={}
openai.api_key=""
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        textLabel=qt.QLabel(_("message"))
        self.message=qt.QLineEdit()
        self.message.setAccessibleName(_("message"))
        self.send=qt.QPushButton(_("send message"))
        self.send.setDefault(True)
        self.send.clicked.connect(self.fsende)
        self.messages=qt.QComboBox()
        self.messages.setAccessibleName(_("messages"))
        self.re=qt.QListWidget()
        self.re.setAccessibleName(_("chatgpt respons"))
        self.messages.currentIndexChanged.connect(self.mel)
        self.copy=qt.QPushButton(_("copy respons"))
        self.copy.setDefault(True)
        self.copy.clicked.connect(lambda:pyperclip.copy(chatm[self.messages.currentText()]))
        self.listen=qt.QPushButton(_("listen"))
        self.listen.setDefault(True)
        self.listen.clicked.connect(self.tts1)
        self.settings=qt.QPushButton(_("settings"))
        self.settings.clicked.connect(self.fsetting)
        self.settings.setDefault(True)
        layout=qt.QVBoxLayout()
        layout.addWidget(textLabel)
        layout.addWidget(self.message)
        layout.addWidget(self.send)
        layout.addWidget(self.messages)
        layout.addWidget(self.re)
        layout.addWidget(self.copy)
        layout.addWidget(self.listen)
        layout.addWidget(self.settings)
        central_widget = qt.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:openLink("https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:openLink("https://t.me/tprogrammers"))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:openLink("https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)

    def tts(self):
        try:
            self.listen.setDisabled(True)
            p="data/12.mp3"
            import google
            import sounddevice as sd
            import soundfile as sf
            google.save(chatm[self.messages.currentText()],p,settings_handler.get("g","langtts"))
            data, samplerate = sf.read(p)
            sd.play(data, samplerate)
            sd.wait()
            os.remove(p)
            self.listen.setDisabled(False)
        except:
            qt.QMessageBox.information(self,_("error"),_("The program is unable to get data from google, the internet may be weak. If the problem persists, you should inform the developer"))
            self.listen.setDisabled(False)
    def fsetting(self):
        self.hide()
        settings.main().exec()
        self.show()
    def fsend(self):
        try:
            winsound.PlaySound("data/sounds/1.wav",0)
            self.send.setDisabled(True)
            self.message.setDisabled(True)
            m=self.message.text()
            re=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role": "system","content": m}],temperature=0.5,max_tokens=3000,top_p=1.0,frequency_penalty=0.0,presence_penalty=0.0)
            chatm[m]=re["choices"][0]["message"]["content"]
            self.messages.clear()
            k=chatm.keys()
            self.messages.addItems(list(k))
            self.re.clear()
            self.messages.setCurrentText(m)
            self.re.setFocus()
            self.send.setDisabled(False)
            self.message.setDisabled(False)
            winsound.PlaySound("data/sounds/2.wav",0)
        except :
            qt.QMessageBox.information(self,_("error"),_("The program is unable to send the message, the internet may be weak. If the problem persists, you should inform the developer"))
            self.send.setDisabled(False)
            self.message.setDisabled(False)
            
    def mel(self):
        self.re.clear()
        try:
            self.re.addItems(chatm[self.messages.currentText()].split("\n"))
        except:
            pass
    def fsende(self):
        thread=threading.Thread(target=self.fsend)
        thread.start()
    def tts1(self):
        if self.messages.count()==0:            
            qt.QMessageBox.information(self,_("error"),_("please select message "))
        else:
            thread=threading.Thread(target=self.tts)
            thread.start()



App=qt.QApplication([])
w=main()
w.show()
App.exec()