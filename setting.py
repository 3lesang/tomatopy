from tkinter import *
import getjson
import components
import json


class newSetting():
    def __init__(self, mainapp):
        self.screenSetting = self.initScreen(mainapp)
        self.saved = False
        self.createComponents()
        self.showComponents()
        self.showData()

    def readData(self):
        data = getjson.readSetting('user.json')
        return data

    def showData(self):
        data = getjson.readSetting('user.json')
        output = str(data)
        self.text.insert(INSERT, output)

    def savedSetting(self):
        data = self.text.get("1.0", "end-1c")
        data = data.replace("\'", "\"")
        output = json.loads(data)
        getjson.writeSetting('user.json', output)
        self.screenSetting.destroy()

    def initScreen(self, mainapp):
        screen = Toplevel(mainapp, bg='#fff')
        screen.iconbitmap('img/setting.ico')
        screen.title('Setting')
        screen.resizable(False, False)
        screen.grab_set()
        return screen

    def createComponents(self):
        self.saveIcon = PhotoImage(file='img/save.png')
        self.saveBtn = components.createIcon(
            self.screenSetting, 'Save', self.saveIcon, self.savedSetting)
        self.text = components.createText(
            self.screenSetting, ('Popins', 12, NORMAL))

    def showComponents(self):
        self.saveBtn.pack()
        self.text.pack(expand=True)
