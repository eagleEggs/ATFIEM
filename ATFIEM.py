import pysftp as ftp
import sys
import PySimpleGUI as sg
from io import StringIO, BytesIO
from time import sleep
from random import randint
import _thread
from paramiko import RSAKey
from base64 import decodebytes
import win32clipboard

enabled = False
autoState = False
streamTime = 10

class Engine(object):
    def __init__(self, host, user, passw):
        self.host = host
        self.user = user
        self.passw = passw
        self.connection = ""
        self.enabled = enabled
        self.active_streaming = False

    def login(self):
        try:
            self.connection = ftp.Connection(self.host, username=self.user,
               password=self.passw, cnopts=cnopts)
            self.connection.cd('files')

            sg.PopupOK("Connected just fine...")

        except :
            e = sys.exc_info()
            sg.PopupError("Unable to Connect, try it again "
                          "greg... {}".format(e))

    def logout(self):
        try:
            self.connection.close()
            sg.PopupOK("disConnected just fine...")
        except:
            e = sys.exc_info()
            sg.PopupError("Unable to disConnect, oops... {}".format(e))

    def threaddd(self, ok, okk):
        self.ok = ok
        self.okk = okk
        while True:
            if self.enabled:
                self.enabled = False
                timesleep = randint(9, 200)
                if timesleep == 20:
                    self.connection.cd('files')
                    print("files")
                if timesleep == 33:
                    listdir = []
                    listdir.append(self.connection.listdir())
                    print(listdir)
                    print("list files")
                if timesleep == 69:
                    self.connection.exists('file.txt')
                    print("exist files")
                if timesleep == 150:
                    self.connection.isdir('files')
                    print("is dir")
                if timesleep == 169:
                    self.connection.isfile('file.txt')
                    print("is file")

                print(print("Polling slept for {}".format(timesleep)))
                sleep(timesleep)
                self.enabled = True
            pass
        pass

    def polling(self):
        ok = "ok"
        _thread.start_new_thread(self.threaddd, ("ok", "okk"))

    def stream_threaddd(self, ok, okk):
        self.ok = ok
        self.okk = okk
        while True:
            sleep(streamTime)
            if autoState:
                if not self.active_streaming:
                    self.active_streaming = True
                    win32clipboard.OpenClipboard()
                    clipData = win32clipboard.GetClipboardData()
                    print("Clipboard Data: {}".format(clipData))
                    outputThing = mainWindow.FindElement('ml')
                    lines = []
                    for line in clipData:
                        lines.append(line)
                    outputThing.Update(''.join(lines))
                    win32clipboard.CloseClipboard()
                    print("Stream slept for {}".format(streamTime))
                    self.active_streaming = False
                pass
            pass

    def streaming(self):
        ok = "ok"
        _thread.start_new_thread(self.stream_threaddd, ("ok", "okk"))

hostList = ["I'm Outside", "I'm Inside"]
mw = [[sg.DropDown(hostList, default_value="I'm Outside",
                   size=(24, 1),
                    key="host"),
       sg.InputText("Enter Your Username Dude(et)", size=(28, 1), key="user"),
       sg.Text("pw:"), sg.InputText("okokok", size=(26,
                                                                        1),
                                    password_char="^",

                      key="pass")],
      [sg.Multiline(size=(87, 21), key="ml")], [sg.Button(
            "Connect",
                                                       key="open"),
                                sg.Button("Disconnect", key="close"),

                                                sg.Text("", size=(18, 1)),
                                sg.Button("Streaming Clipboard: OFF",
                                          button_color=("White",
                                                                 "Red"),
                                          key="auto"),
                                sg.Button("Copy Down", key="pull"),
                                sg.Button("Paste Up", key="push")
                                ]]

mainWindow = sg.Window("ATFIEM - Around the FTP", layout=mw).Finalize()

while True:
    b, values = mainWindow.Read(timeout=100)

    if b == "open":
        if not enabled:
            enabled = True
            if values['host'] == "I'm Outside":

                keydataOUT = b"""PUBLICKEY"""
                keyOUT = RSAKey(data=decodebytes(keydataOUT))
                cnopts = ftp.CnOpts()
                cnopts.hostkeys.add('EXTHOSTNAME', 'ssh-rsa',
                                    keyOUT)
                hostPoint = "EXTHOSTNAME"
            else:

                keydataIN = b"""PUBLICKEY"""
                keyIN = RSAKey(data=decodebytes(keydataIN))
                cnopts = ftp.CnOpts()
                cnopts.hostkeys.add('INHOSTNAME', 'ssh-rsa', keyIN)
                hostPoint = "INHOSTNAME"

            ignite = Engine(hostPoint, values["user"], values["pass"])
            ignite.login()
            ignite.polling()

    if b == "close":
        try:
            enabled = False
            ignite.logout()
            sg.PopupOK("Logged Out")
        except:
            pass

    if b == "push":
        try:
            ignite.connection.putfo(StringIO(values['ml']), '/files/file.txt')
            sg.PopupOK("Pushed good")
        except:
            sg.PopupError("Unable to push")

    if b == "pull":
        try:
            data = BytesIO()
            superdata = ignite.connection.open('/files/file.txt')
            outputThing = mainWindow.FindElement('ml')
            lines= []
            for line in superdata:
                lines.append(line)
            outputThing.Update(''.join(lines))
            sg.PopupOK("Pulled good")
        except:
            sg.PopupError("Unable to Pulllllll")

    if b == "auto":
        if not autoState:
            autoState = True
            mainWindow.FindElement("auto").Update(
                button_color=("White",
                              "Green"))
            mainWindow.FindElement("auto").Update("Streaming Clipboard: ON  ")
            ignite.streaming()

        else:
            autoState = False
            mainWindow.FindElement("auto").Update(
                    button_color=("White",
                                  "Red"))
            mainWindow.FindElement("auto").Update("Streaming Clipboard: OFF")

    if b != sg.TIMEOUT_KEY:
        pass

    if b is None:
        enabled = False
        break

    if b == "exit":
        enabled = False
        try:
            ignite.logout()
        except:
            pass

        break

    else:
        pass
