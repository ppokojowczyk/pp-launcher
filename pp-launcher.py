#!/usr/bin/env python
import Tkinter as tk
from subprocess import Popen
from PIL import Image
import ConfigParser as cp
import re
import ast
import os
import os.path

class PpLauncher(tk.Frame):

    #
    # Icon (item) class.
    #
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
    currentPath = ''

    #
    # Main function.
    #
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg='#000000')
        if(self.checkConfig() == False):
            self.quit()
        root = self.master
        self.currentPath = os.path.dirname(os.path.realpath(__file__)) + '/';
        root.wm_attributes('-type', 'normal')
        root.wm_attributes('-fullscreen', True)
        root.attributes('-alpha', 1)
        root.update_idletasks()
        screenWidth, screenHeight = root.winfo_width(), root.winfo_height()
        self.config(width=screenWidth, height=screenHeight)
        self.grid(sticky='n')
        root.wait_visibility(root)
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-alpha", 0.9)
        root.config(bg='#000000')
        self.loadConfig()
        self.initIcons()
        self.initPanel()
        self.renderIcons()
        self.bindKeys()

    #
    # Check if configuration is valid.
    # __TODO__ this should check if everything is ok; valid config exists?
    #
    def checkConfig(self):
        return False

    #
    # Initialize status icon in tray.
    # __TODO__ yet to be done
    #
    def initStatusIcon(self):
        return

    #
    # Set keys bindings.
    #
    def bindKeys(self):
        self.master.bind('<Escape>', lambda e:self.quit())
        self.master.bind('<q>', lambda e:self.quit())
        self.master.bind('<Right>', lambda e:self.nextIcon())
        self.master.bind('<Left>', lambda e:self.prevIcon())
        self.master.bind('<l>', lambda e:self.nextIcon())
        self.master.bind('<j>', lambda e:self.prevIcon())
        self.master.bind('<Return>', lambda e:self.executeCommand(self.icons[self.currentIconIndex]))

    def renderIcon(self, icon, column):

        # Check if icon file exists; if not then use generic one
        if(os.path.isfile(icon.icon)):
            image = tk.PhotoImage(file=icon.icon)
        else:
            image = tk.PhotoImage(file=self.currentPath + 'icon-1.png')

        btn = tk.Button(self.panel, text=icon.name, fg='#ffffff', bd=0, height=64, command=lambda icon=icon: self.executeCommand(icon), image=image, relief='flat', bg='#000000')

        if(self.config.get('Main', 'ShowText') == 'true'):
            btn.config(compound='left')
        else:
            btn.config(width=64)

        btn.config(highlightbackground='#000000')
        btn.config(activebackground='#000000')
        btn.config(activeforeground='#ffffff')
        btn.config(highlightcolor=self.config.get('Main', 'ItemBorderColor'))
        btn.config(highlightthickness=2)
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
            params = icon.cmd.split(" ")
            Popen(params)
            self.quit()
        return

    def initPanel(self):
        self.panel = tk.Frame(self.master, borderwidth=0, relief="sunken", bg='')
        self.panel.grid(row=0)

    #
    # Get config option value.
    #
    def getOption(self, optionName):
        sectionName = "Main";
        if(self.config.has_option(sectionName, optionName)):
            return self.config.get(sectionName, optionName);
        return None; # or False?

    def initIcons(self):
        if(self.getOption("ShowCloseButton") == "true"):
            self.icons.append( self.Icon(name='Close', icon=self.currentPath + '/icons/close.png', cmd='app.quit') )
        else:
            return

    def loadConfig(self):
        config = cp.ConfigParser()
        path = './pp-launcher.conf'
        config.read(path)
        self.config = config;
        self.loadItemsFromConfig(config)
        return

    def loadItemsFromConfig(self, config):
        tmp = config.get('Items', 'Items')
        items = ast.literal_eval(tmp)
        for item in items:
            newIcon = self.Icon()
            if('name' in item):
                newIcon.name = item['name']
            if('icon' in item):
                newIcon.icon = item['icon']
            if('cmd' in item):
                newIcon.cmd = item['cmd']
            self.icons.append( newIcon )
        return

app = PpLauncher()
app.master.title('pp-launcher')
app.mainloop()
