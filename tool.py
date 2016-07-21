#!/usr/bin/python3
# feedback_solution.py by Barron Stone
# This is an exercise file from Python GUI Development with Tkinter on lynda.com

import datetime
import configparser
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from ext.TimeManager import TimeManager
from ext.MainManager import MainManager
from ext.AlarmManager import AlarmManager
from ext.VoiceManager import VoiceManager
from ext.YandexNewsManager import YandexNewsManager

class App(object):
    """description of class"""
    def __init__(self):
        self._config = None
        self._root = Tk()
        self._root.title('DashBoard Tool')
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)
        
        self._window = Frame(self._root)
        self._window.grid(row=0, column=0, sticky=NSEW)
        self._window.rowconfigure(1, weight=1)
        self._window.columnconfigure(0, weight=1)

        header = LabelFrame(self._window, text="Configuration", bg = "blue", width=300, height=100)
        header.grid(row=0, column=0, sticky=NSEW)
        header.columnconfigure(4, weight=1)

        entryFileName = Entry(header, width=24)
        entryFileName.grid(row=0, column=0, padx=2, pady=2)
        
        btnSelect = Button(header, text="...", command=self.loadFile)
        btnSelect.grid(row=0, column=1, padx=2, pady=2)

        btnLoad = Button(header, text= " Load ", command=self.showData1)
        btnLoad.grid(row=0, column=2, padx=2, pady=2)

        btnSave = Button(header, text= " Save ", command=self.showData2)
        btnSave.grid(row=0, column=3, padx=2, pady=2)

        self._text = Text(self._window, wrap=NONE)
        self._text.grid(row=2, column=0, sticky=NSEW)

        self._root.bind('<Key-Escape>', lambda e: self._root.destroy())
        #self._root.resizable(False, False)
        self._root.geometry("+0+0")
    
    def run(self):
        self._root.mainloop()


    def loadFile(self): 
        fn = filedialog.Open(self._root, filetypes = [('*.ini files', '.ini')]).show()
        if fn == '': return
        self._config = configparser.ConfigParser()
        self._config.read(fn, encoding="utf-8")
        self._text.delete('1.0', 'end') 
        self._text.insert('1.0', open(fn, 'rt').read())

    def showData1(self): 
        #self.dlg = MainManager(self._window)
        #self.dlg = AlarmManager(self._window)
        #self.dlg = TimeManager(self._window)
        self.dlg = VoiceManager(self._window)
        self.dlg.grid(row=1, column=0, sticky=(N,S,E,W))
        self.dlg.load(self._config)

    def showData2(self): 
        config = configparser.ConfigParser()
        self.dlg.save(config)
        with open('new_setting.ini', 'w') as fp:
            config.write(fp)
        self._text.delete('1.0', 'end') 
        self._text.insert('1.0', open('new_setting.ini', 'rt').read())

def main():            
    App().run()
    
if __name__ == "__main__":
    main()
