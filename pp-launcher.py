#!/usr/bin/env python
import Tkinter as tk
from subprocess import Popen
from PIL import Image

class PpLauncher(tk.Frame):

    # icon (item) class
    class Icon():
        def __init__(self, name = '', cmd = '', icon = ''):
            self.name = name
            self.cmd = cmd
            self.icon = icon
        name = ''
        cmd = ''
        icon = ''
        btn = tk.Button

    icons = [] # all icons should be kept here
    iconsCount = 0
    currentIconIndex = 0

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, width=1920, bg='#000000', height=1080)
        root = self.master

        screenWidth, screenHeight = root.winfo_screenwidth(), root.winfo_screenheight()
        root.wm_attributes('-type', 'normal')
        root.wm_attributes('-fullscreen', True)
        self.config(width=screenWidth, height=screenHeight)
        # root.overrideredirect(True)
        # self.place(y=5000)
        self.grid(sticky='n')
        root.wait_visibility(root)
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-alpha", 0.9)
        root.config(bg='#000000')
        self.initIcons()
        self.initPanel()
        self.renderIcons()
        self.bindKeys()

    def initStatusIcon(self):
        return

    def bindKeys(self):
        self.master.bind('<Escape>', lambda e:self.quit())
        self.master.bind('<Right>', lambda e:self.nextIcon())
        self.master.bind('<Left>', lambda e:self.prevIcon())
        self.master.bind('<Return>', lambda e:self.executeCommand(self.icons[self.currentIconIndex]))

    def renderIcon(self, icon, column):
        image = tk.PhotoImage(file=icon.icon)
        btn = tk.Button(self.panel, text=icon.name, bd=0, width=64, height=64, command=lambda icon=icon: self.executeCommand(icon), image=image, relief='flat', bg='#000000')
        btn.config(highlightbackground='#000000')
        btn.config(activebackground='#000000')
        btn.config(highlightcolor='#5895FF')
        btn.config(highlightthickness=3)
        btn.image = image
        btn.grid(row=0, column=column, padx=10, pady=10)
        icon.button = btn
        return

    def iconFocus(self, index):
        self.currentIconIndex = index
        return

    def renderIcons(self):
        column = 0;
        for icon in self.icons:
            self.iconsCount = self.iconsCount + 1
            self.renderIcon(icon, column)
            if(column == 0):
                self.icons[0].button.focus_set()
                self.currentIconIndex = 0
            self.icons[column].index = column
            self.icons[column].button.bind('<FocusIn>', lambda e, index=column :self.iconFocus(index))
            column = column+1

    def focusButton(self, index):
        self.icons[index].button.focus_set()

    def nextIcon(self):
        self.currentIconIndex = self.currentIconIndex + 1
        if((self.currentIconIndex+1) > self.iconsCount):
            self.currentIconIndex = 0
        self.icons[self.currentIconIndex].button.focus_set()

    def prevIcon(self):
        self.currentIconIndex = self.currentIconIndex - 1
        if(self.currentIconIndex < 0):
            self.currentIconIndex = self.iconsCount - 1
        self.icons[self.currentIconIndex].button.focus_set()

    def executeCommand(self, icon):

        if(icon.cmd == 'app.quit'):
            self.quit()
            return

        if(icon.cmd):
            Popen(icon.cmd)
            self.quit()
        return

    def initPanel(self):
        self.panel = tk.Frame(self.master, borderwidth=0, relief="sunken", bg='')
        self.panel.grid(row=0)

    def initIcons(self):
        #self.icons.append( self.Icon(name='Bluefish', icon='/usr/share/icons/hicolor/64x64/apps/bluefish.png', cmd='bluefish') )
        self.icons.append( self.Icon(name='Smplayer', icon='/usr/share/icons/hicolor/64x64/apps/smplayer.png', cmd='smplayer') )
        self.icons.append( self.Icon(name='Smplayer', icon='/usr/share/icons/hicolor/64x64/apps/smplayer.png', cmd='smplayer') )
        self.icons.append( self.Icon(name='Close', icon='/usr/share/icons/hicolor/48x48/apps/system-shutdown.png', cmd='app.quit') )

app = PpLauncher()
app.master.title('pp-launcher')
app.mainloop()
