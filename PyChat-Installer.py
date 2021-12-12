#!/usr/bin/env python3
import sys
from os.path import join, exists, expanduser
from subprocess import call
if len(sys.argv) == 1:

    print(" ╔════════════════════════════════════════════════════════════════════════════════════╗")
    print(" ║                                  >> BENVENUTO! <<                                  ║")
    print(" ╠════════════════════════════════════════════════════════════════════════════════════╣")
    print(" ║                  Grazie per aver scelto di installare quest'app.                   ║")
    print(" ║             Se hai un qualsiasi dubbio o curiosità, hai trovato un bug             ║")
    print(" ║            o vuoi semplicamente passare a salutare, scrivimi su Discord!           ║")
    print(" ║                                     neeco#7533                                     ║")
    print(" ╠════════════════════════════════════════════════════════════════════════════════════╣")
    print(" ║ Assicurati di essere connesso a Internet.                                          ║")
    print(" ║ Non chiudere questa finestra fino a quando l'installazione non sarà completata.    ║")
    print(" ╠════════════════════════════════════════════════════════════════════════════════════╣")
    print(" ║ Premi <Invio> per continuare.                                                      ║")
    input(" ╚════════════════════════════════════════════════════════════════════════════════════╝\n")

    if not exists('C:\\Windows\\Fonts\\Product Sans Regular.ttf'):
        print(" ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗")
        print(" ║                                        * Attenzione *                                                 ║")
        print(" ╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣")
        print(' ║ Questa applicazione utilizza il font "Product Sans", che non è preinstallato nel sistema.             ║')
        print(' ║ Per una migliore esperienza è consigliato di installarlo manualmente, dato che questo programma       ║')
        print(' ║ non è ancora in grado di farlo automaticamente.                                                       ║')
        print(' ║ Il file può essere trovato nella cartella "'+ join(expanduser('~'), '.PyChat', 'fonts."').ljust(59) +'║')
        input(" ╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝\n")


    if sys.platform.startswith('linux'):
        if call(['which', 'pip']) == 1:
            call(['sudo', 'apt-get', 'install', 'python3-pip'])
    cmd = [sys.executable, '-m', 'pip', 'install', 'pyqt5-tools', 'qtmodern', 'requests']
    if sys.platform == 'win32': 
        cmd.append('pywin32')
    if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
        cmd.append('--user')
        cmd.append('--no-warn-script-location')
    call(cmd)
    call([sys.executable, __file__, ':)'])
    exit()

try: import PyQt5.QtGui
except Exception as e: input(f'\nErrore durante l\'installazione. Controlla i messaggi in rosso qui sopra per i dettagli.\n{type(e).__name__}: {e}'); exit()
import PyQt5.QtWidgets
import PyQt5.QtCore
from base64 import b64decode
from os import mkdir, chdir
from threading import Thread
from requests import get, exceptions
from socket import socket, timeout


path = join(expanduser('~'), '.PyChat')
buf = 1024


class LoadingSignals(PyQt5.QtCore.QObject):
    setLabel = PyQt5.QtCore.pyqtSignal(str)
    setProgress = PyQt5.QtCore.pyqtSignal(int)
    ext = PyQt5.QtCore.pyqtSignal(int)

    def __init__(self):
        super(LoadingSignals, self).__init__()


loadingscreen = LoadingSignals()


class Ui_MainWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setWindowFlags(PyQt5.QtCore.Qt.FramelessWindowHint | PyQt5.QtCore.Qt.WindowStaysOnTopHint | PyQt5.QtCore.Qt.Tool)
        self.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground)
        self.setupUi()
        self.show()

    def setupUi(self):
        self.resize(448, 255)
        self.setStyleSheet(
            "QFrame{border: none;border-top-left-radius: 13px;border-top-right-radius: 13px;background-color: qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0.23,stop:0 rgb(33, 37, 41),stop:1 rgb(46, 57, 62))}"
            "QLabel{font-family: Product Sans; font-size: 20px; color: #fff; padding-left: 15; padding-right: 15; background: none}"
            "QLabel#sub{font-size: 13px}"
            "QProgressBar {color: #00ffffff; border: none; border-radius: 3px; background: rgb(46, 57, 62)}"
            "QProgressBar::chunk {background: rgb(236, 162, 71); border-radius: 3px}")
        self.frame = PyQt5.QtWidgets.QFrame(self)
        self.mainLayout = PyQt5.QtWidgets.QGridLayout(self.frame)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.progressBar = PyQt5.QtWidgets.QProgressBar(self.frame)
        self.progressBar.setMaximumSize(PyQt5.QtCore.QSize(448, 6))
        self.progressBar.setProperty('value', 0)
        self.anim = PyQt5.QtCore.QPropertyAnimation(self.progressBar, b'value')
        self.anim.setEasingCurve(PyQt5.QtCore.QEasingCurve.InOutSine)
        self.anim.setDuration(300)
        self.value = 0
        self.mainLayout.addWidget(self.progressBar, 5, 0, 1, 3)
        self.subtitle = PyQt5.QtWidgets.QLabel(self.frame)
        self.subtitle.setObjectName('sub')
        self.subtitle.setText('Connessione al server...')
        self.subtitle.setMinimumSize(PyQt5.QtCore.QSize(0, 130))
        self.subtitle.setAlignment(PyQt5.QtCore.Qt.AlignRight | PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignTrailing)
        self.mainLayout.addWidget(self.subtitle, 4, 0, 1, 3)
        self.title = PyQt5.QtWidgets.QLabel(self.frame)
        self.title.setText('PyChat Installer')
        self.title.setSizePolicy(PyQt5.QtWidgets.QSizePolicy(PyQt5.QtWidgets.QSizePolicy.Preferred, PyQt5.QtWidgets.QSizePolicy.Maximum))
        self.title.setMinimumSize(PyQt5.QtCore.QSize(0, 100))
        self.title.setAlignment(PyQt5.QtCore.Qt.AlignBottom | PyQt5.QtCore.Qt.AlignLeading | PyQt5.QtCore.Qt.AlignLeft)
        self.mainLayout.addWidget(self.title, 0, 0, 2, 3)
        self.line = PyQt5.QtWidgets.QFrame(self.frame)
        self.line.setSizePolicy(PyQt5.QtWidgets.QSizePolicy(PyQt5.QtWidgets.QSizePolicy.Preferred, PyQt5.QtWidgets.QSizePolicy.Fixed))
        self.line.setMaximumSize(PyQt5.QtCore.QSize(16777215, 2))
        self.line.setStyleSheet('background-color: qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 rgb(252, 53, 129),stop:1 rgb(236, 162, 71));')
        self.line.setFrameShape(PyQt5.QtWidgets.QFrame.HLine)
        self.mainLayout.addWidget(self.line, 2, 0, 2, 3)
        self.setCentralWidget(self.frame)

        loadingscreen.setProgress.connect(self.setProgress)
        loadingscreen.setLabel.connect(self.setLabel)
        loadingscreen.ext.connect(self.badexit)

    def mousePressEvent(self, event):
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseMoveEvent(self, event):
        self.move(event.globalX()-self.x0, event.globalY()-self.y0)

    def setLabel(self, text):
        self.subtitle.setText(text)

    def setProgress(self, value):
        if value == 100:
            self.anim.setDuration(500)
            self.anim.finished.connect(self.exit)
            self.setLabel('Avvio...')
        self.anim.setStartValue(self.value)
        self.value = value
        self.anim.setEndValue(self.value)
        self.anim.start()

    def exit(self, aight=True):
        self.close()
        if aight:
            call([sys.executable, 'main.py'])
        exit()

    def badexit(self, code):
        if code == 1:
            msg = 'Offline  -  Server non attivo'
        elif code == 2:
            msg = 'Offline  -  Nessuna connessione a Internet'
        elif code == 3:
            msg = 'Offline  -  Nessuna risposta dal Server'
        self.setLabel(msg)
        self.anim.setStartValue(self.value)
        self.anim.setEndValue(100)
        self.anim.setDuration(3000)
        self.anim.finished.connect(lambda: self.exit(False))
        self.anim.start()


def connect():
    global sock, users
    sock = socket(2, 1)
    sock.settimeout(5)
    try: sock.connect((b64decode(get('https://raw.githubusercontent.com/nkoexe/nkoexe/main/data.txt').text.encode()), 9835))
    except ConnectionRefusedError: return loadingscreen.ext.emit(1)
    except exceptions.ConnectionError: return loadingscreen.ext.emit(2)
    except timeout: return loadingscreen.ext.emit(3)
    sock.settimeout(None)

    sock.recv(buf)
    sock.send(b'-1')
    loadingscreen.setLabel.emit('Scaricando i dati...')
    progress = 15
    loadingscreen.setProgress.emit(progress)

    if not exists(path): mkdir(path)
    chdir(path)
    for i in ['main.py', 'widgets.py', 'config.py']:
        with open(i, 'wb') as f:
            while True:
                l = sock.recv(buf)
                if l[-3:] == b'$$$':
                    f.write(l[:-3])
                    break
                f.write(l)
        sock.send(b'k')

    progress += 10
    loadingscreen.setProgress.emit(progress)

    for j in ['ui', 'icons', 'fonts']:
        files = sock.recv(buf).decode().split('@')
        sock.send(b'k')
        for i in files:
            if not exists(j): mkdir(j)
            with open(join(j, i), 'wb') as f:
                while True:
                    l = sock.recv(buf)
                    if l[-3:] == b'$$$':
                        f.write(l[:-3])
                        break
                    f.write(l)
            sock.send(b'k')
        progress += 20
        loadingscreen.setProgress.emit(progress)


    # TODO: install Fonts

    if sys.platform == 'win32':
        from win32com.client import Dispatch
        for i in [join(expanduser('~'), 'Desktop', 'PyChat.lnk'), join(expanduser('~'), 'AppData\Roaming\Microsoft\Windows\Start Menu\Programs', 'PyChat.lnk')]:
            shortcut = Dispatch('WScript.Shell').CreateShortCut(i)
            shortcut.Targetpath = join(path, 'main.py')
            shortcut.WorkingDirectory = path
            shortcut.IconLocation = join(path, 'icons', 'appicon.ico')
            shortcut.save()
    elif sys.platform.startswith('linux'):
        open(join(expanduser('~'), 'Desktop', 'PyChat.desktop'), 'w').write(f'''[Desktop Entry]
Name=PyChat
Icon={expanduser('~')}/.PyChat/icons/appicon.ico
Exec=python3 {expanduser('~')}/.PyChat/main.py
Terminal=true
Type=Application''')
        call(['chmod', '+x', join(expanduser('~'), 'Desktop', 'PyChat.desktop')])

    loadingscreen.setProgress.emit(100)


app = PyQt5.QtWidgets.QApplication([])
win = Ui_MainWindow()
Thread(target=connect).start()
app.exec_()
