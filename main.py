from tkinter import *
from tkinter import filedialog
import vlc

import components
from setting import newSetting
import getjson
app = Tk()


class Tomato:
    def __init__(self, app):
        self.mainApp = app
        self.pathLogoIcon = 'img/tomato.ico'
        self.pathPlayButtonIcon = 'img/play.png'
        self.pathStopButtonIcon = 'img/stop.png'
        self.pathSettingButtonIcon = 'img/setting.png'
        self.pathRefreshButtonIcon = 'img/refresh.png'
        self.pathMusicButtonIcon = 'img/music.png'
        self.pathSounds = 'sound/'
        self.media_player = vlc.MediaListPlayer()
        self.media = self.media_player.get_media_player()
        self.state = 0
        self.timeCount = 0
        self.timeInit = self.timeCount
        self.initTime = self.getTime()
        self.onTime = None
        self.createComponents()
        self.showComponents()
        self.refresh()
        self.configApp('Tomato')

    def configApp(self, title):
        self.mainApp.title(title)
        # app.resizable(False, False)
        self.mainApp.iconbitmap(self.pathLogoIcon)

    def createComponents(self):
        self.frameStopPlay = components.createFrame(self.mainApp)
        self.frameNav = components.createFrame(self.mainApp)
        self.frameOption = components.createFrame(self.mainApp)
        self.volume = Scale(self.frameOption, orient=HORIZONTAL, cursor='hand2',
                            bd=0, length=150, showvalue=0, width=8, highlightthickness=0, troughcolor='#ddd', sliderrelief=FLAT, command=self.controlVolume)
        self.volume.set(50)
        self.media.audio_set_volume(self.volume.get())
        self.playButtonIcon = PhotoImage(file=self.pathPlayButtonIcon)
        self.stopButtonIcon = PhotoImage(file=self.pathStopButtonIcon)
        self.settingButtonIcon = PhotoImage(file=self.pathSettingButtonIcon)
        self.refreshButtonIcon = PhotoImage(file=self.pathRefreshButtonIcon)
        self.musicButtonIcon = PhotoImage(file=self.pathMusicButtonIcon)
        self.btnFocus = components.createFormalButton(
            self.frameNav, 'Tomato', self.startFocus)
        self.btnShortBreak = components.createFormalButton(
            self.frameNav, 'Short Break', self.startShortBreak)
        self.btnLongBreak = components.createFormalButton(
            self.frameNav, 'Long Break', self.startLongBreak)
        self.timeDisplay = components.createLabel(
            self.mainApp, self.initTime, ('Poppins', 72, 'bold'))
        self.playBtn = components.createIcon(
            self.frameStopPlay, 'Start', self.playButtonIcon, self.onMode)
        self.stopBtn = components.createIcon(
            self.frameStopPlay, 'Stop', self.stopButtonIcon, self.stop)
        self.settingBtn = components.createIcon(
            self.frameOption, 'Setting', self.settingButtonIcon, self.setting)
        self.refreshBtn = components.createIcon(
            self.frameOption, 'Refresh', self.refreshButtonIcon, self.refresh)
        self.musicBtn = components.createIcon(
            self.frameOption, 'Music', self.musicButtonIcon, self.playMusic)

    def showComponents(self):
        self.timeDisplay.pack(side=TOP)
        self.frameStopPlay.pack(pady=16)
        self.playBtn.pack()
        self.settingBtn.pack(side=LEFT, padx=16)
        self.refreshBtn.pack(side=LEFT, padx=16)
        self.musicBtn.pack(side=LEFT, padx=16)
        self.btnFocus.pack(side=LEFT)
        self.btnShortBreak.pack(side=LEFT)
        self.btnLongBreak.pack(side=LEFT)
        self.volume.pack(side=LEFT)
        self.frameNav.pack()
        self.frameOption.pack(pady=16)

    def refresh(self):
        self.data = self.loadSetting()
        self.data["work"] = self.data["work"] * 60
        self.data["short"] = self.data["short"] * 60
        self.data["long"] = self.data["long"] * 60
        self.colors = self.data["colors"]
        self.sounds = self.data["sounds"]
        self.iSound = self.data["soundIndex"]
        self.longInterval = self.data["longInterval"]
        self.mainApp.configure(bg=self.colors[0])
        self.mainApp.wm_attributes(
            '-transparentcolor', self.data["transparent"])

    def loadSetting(self):
        data = getjson.readSetting('settings.json')
        return data

    def setting(self):
        self.resetTime()
        config = newSetting(self.mainApp)

    def getTime(self):
        minute = self.timeCount // 60
        second = self.timeCount % 60
        secondStr = ''
        minuteStr = ''
        if(minute < 10):
            minuteStr = '0' + str(minute)
        else:
            minuteStr = str(minute)
        if(second < 10):
            secondStr = '0' + str(second)
        else:
            secondStr = str(second)
        string = minuteStr + ':' + secondStr
        return string

    def onMode(self):
        self.stopBtn.pack()
        self.playBtn.pack_forget()
        if(self.onTime == None):
            if(self.state == 0):
                self.startFocus()
            elif(self.state == 1):
                self.startShortBreak()
            else:
                self.startLongBreak()

    def stop(self):
        self.playBtn.pack()
        self.stopBtn.pack_forget()
        self.state = 0
        self.resetTime()

    def startTime(self):
        if(self.timeCount >= 0):
            string = self.getTime()
            self.timeDisplay.config(text=string)
            self.timeCount -= 1
            self.onTime = self.timeDisplay.after(1000, self.startTime)
        else:
            self.playSound()
            self.onTime = None
            self.onMode()

    def startFocus(self):
        self.stopBtn.pack()
        self.playBtn.pack_forget()
        self.btnFocus.config(bg='red', fg='white')
        self.btnShortBreak.config(bg=self.colors[0], fg='#000')
        self.btnLongBreak.config(bg=self.colors[0], fg='#000')
        self.timeCount = self.data["work"]
        self.timeInit = self.timeCount
        self.longInterval -= 1
        if(self.longInterval == 0):
            self.state = 2
        else:
            self.state = 1
        self.resetTime()
        self.startTime()

    def startShortBreak(self):
        self.stopBtn.pack()
        self.playBtn.pack_forget()
        self.btnShortBreak.config(bg='red', fg='white')
        self.btnFocus.config(bg=self.colors[0], fg='#000')
        self.btnLongBreak.config(bg=self.colors[0], fg='#000')
        self.timeCount = self.data["short"]
        self.timeInit = self.timeCount
        self.state = 0
        self.resetTime()
        self.startTime()

    def startLongBreak(self):
        self.stopBtn.pack()
        self.playBtn.pack_forget()
        self.btnLongBreak.config(bg='red', fg='white')
        self.btnFocus.config(bg=self.colors[0], fg='#000')
        self.btnShortBreak.config(bg=self.colors[0], fg='#000')
        self.timeCount = self.data["long"]
        self.timeInit = self.timeCount
        self.state = 0
        self.longInterval = 4
        self.resetTime()
        self.startTime()

    def playSound(self):
        soundName = self.pathSounds+self.sounds[self.iSound]
        media = vlc.MediaPlayer(soundName)
        media.play()

    def playMusic(self):
        if(self.media_player.is_playing()):
            self.media_player.stop()
        player = vlc.Instance()
        media_list = player.media_list_new()
        self.fileNames = filedialog.askopenfilenames(
            initialdir='/', title='Select a list file music', filetypes=(('Mp3 file', '.mp3'), ('Wav file', '.wav')))
        if(self.fileNames):
            for file in self.fileNames:
                music = player.media_new(file)
                media_list.add_media(music)
            self.media_player.set_media_list(media_list)

            self.media_player.play()

    def controlVolume(self, value=None):
        number = self.volume.get()
        media = self.media_player.get_media_player()
        media.audio_set_volume(number)

    def resetTime(self):
        self.timeCount = self.timeInit
        string = self.getTime()
        self.timeDisplay.config(text=string)
        if(self.onTime):
            self.timeDisplay.after_cancel(self.onTime)
        self.onTime = None


tomato = Tomato(app)
app.mainloop()
